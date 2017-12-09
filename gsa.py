import database as gsa
import urllib.request
import datetime
from bs4 import BeautifulSoup
import data_format
import re

def scrapGSA():
    print("#========================= GSA SCRAPING =========================")

    # Database connection and agency retrieval

    gsaData = gsa.returnAgency('GSA')
    gsa_link = gsaData['link'][0]
    gsa_id = gsaData['id'][0]

    pages = {"CATA": "gsa/jobs-opportunities", "TR": "traineeship-listing", "SNE": "gsa-seconded-national-experts"}

    for pairs in pages:
        title = pairs.title().upper()
        page_link = (gsa_link + "/" + pages[title])


        html = urllib.request.urlopen(page_link)
        soup = BeautifulSoup(html, "html.parser")


        # Create the soup
        start = soup.find('tbody')
        today = datetime.datetime.today().date()


        # Find the jobs table
        Jobtable = (start.findAll('tr'))

        for cell in Jobtable:

            td = cell.findAll('td')
            print (td[0])
'''
            try:
                status = td[3].string.strip()
                rawDate = td[2].string
                searchDate = re.match(r'(.*)at', rawDate)
                date = data_format.dateFormatFull(searchDate.group(1).strip())
            except:
                continue

            if (today < date) and (status == "ongoing"):

                jobLink = gsa_link[:24] + td[0].a.get('href')
                jobTitle = td[0].string
                jobCode = td[1].string.strip()
                jobDeadline = date
                jobType = title
                print(jobCode, jobTitle, jobType, jobDeadline, jobLink)
                gsa.persist(int(gsa_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)
            else:
                continue

    print("#========================EBA SCRAPING COMPLETE=================================")
'''
scrapGSA()