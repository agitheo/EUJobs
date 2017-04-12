import database as emsa
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import data_format


def scrapEMSA():

    print("#========================= EMSA SCRAPING =========================")

    emsaData = emsa.returnAgency('EMSA')
    emsa_link = emsaData['link'][0]
    emsa_id = emsaData['id'][0]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    headers = { 'User-Agent' : user_agent }
    data = ''
    data = data.encode('ascii')


    req = urllib.request.Request(emsa_link,data,headers)

    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "html.parser")



    # Find the first ad
    start = soup.findAll(attrs={"class":"sectiontableentry"})


    # Iterate through the tables
    for cell in start:
        ad_code = cell.find("th").get_text()
        print ("Job Code:" + ad_code.strip())
        ad_url = "http://www.emsa.europa.eu"+cell.find('a').get('href')
        print ("Job URL:" + ad_url)
        count = 0
        for ad in cell.findAll("td"):
            if count == 0 :
                ad_description = ad.get_text()
                print ("description: " + ad_description)
            if count == 2 :
                ad_deadline = ad.get_text()
                print ("deadline: " + ad_deadline)
            count = count + 1

    # Convert date
        try:
            date_object = datetime.strptime(ad_deadline, '%d.%m.%Y')
            deadline = date_object.date()
            #print (deadline)
        except:
            print ("could not modify " + deadline)
            pass

        ad_raw = ad_code +" "+ ad_description
    # Identify type
        jobType = data_format.typeOfGrade(ad_raw)

        print (jobType)

             # Insert job details in database
        emsa.persist(int(emsa_id), str(ad_description).strip(), '', '', str(ad_code).strip(), deadline, str(ad_url).strip(), '', jobType)

    print("#========================EMSA SCRAPING COMPLETE=================================")



