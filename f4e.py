import database as F4E
import re
import urllib
import urllib.request
from bs4 import BeautifulSoup
import data_format



def scrapF4E():

    print("#========================= F4E SCRAPING =========================")

    F4EData = F4E.returnAgency('F4E')
    F4E_link = F4EData['link'][0]
    F4E_id = F4EData['id'][0]

    html = urllib.request.urlopen(F4E_link)
    soup = BeautifulSoup(html, "html.parser")



    start = soup.findAll(attrs={"class": re.compile("^careersPurple2")})

    for contractType in start:

        deadline = jobTitle = jobCode = jobLink = ''
        contract = data_format.typeOfPost(contractType.a.string)

        jobInfo = contractType.next_sibling.next_sibling
        try:
            deadline = data_format.dateFormatFull(jobInfo.find(attrs={"class": "careersDate"}).span.string)
            jobTitle = jobInfo.find(attrs={"class": "careersTitle"}).string
            jobCode = jobInfo.find(attrs={"class": "pdf"}).string
            jobLink = "http://fusionforenergy.europa.eu/careers/vacancies/" + jobInfo.find(attrs={"class": "pdf"}).get("href")
            print(deadline, jobTitle.strip(), jobCode, jobLink,contract)
            F4E.persist(F4E_id, jobTitle.strip(), jobCode,'', '', deadline, jobLink,'',contract)

        except:
            pass
    print("#========================F4E SCRAPING COMPLETE=================================")




