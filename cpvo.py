import database as cpvo
import urllib.request
from bs4 import BeautifulSoup
import data_format
import logging

def scrapCPVO():

    print("#========================= CPVO SCRAPING =========================")

    # Database connection and agency retrieval

    cpvoData = cpvo.returnAgency('CPVO')
    cpvo_link = cpvoData['link'][0]
    cpvo_id = cpvoData['id'][0]

    html = urllib.request.urlopen(cpvo_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('table',attrs={'summary':'Vacancies'})

    # Find the jobs table
    Jobtable = (start.findAll('tr'))

    for child in Jobtable:
        if(child.find('th',attrs={'id':'vacancy_title'})):
            continue
        #print (child)
        jobTitle = child.td.a.string.strip()
        jobLink = child.td.a.get('href')
        jobCode = child.td.next_sibling.next_sibling.string.strip()
        jobType = data_format.typeOfPost(jobCode)
        jobDeadline = data_format.dateFormatFull(child.td.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string.strip())

        logging.debug (jobTitle,jobLink,jobCode,jobType,jobDeadline)
        cpvo.persist(int(cpvo_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)

    print("#========================CPVO SCRAPING COMPLETE=================================")
