import database as esma
import urllib.request
from bs4 import BeautifulSoup
import data_format
import re

def scrapESMA():

    print("#========================= ESMA SCRAPING =========================")

    # Database connection and agency retrieval

    esmaData = esma.returnAgency('ESMA')
    esma_link = esmaData['link'][0]
    esma_id = esmaData['id'][0]

    html = urllib.request.urlopen(esma_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('div',attrs={'class':'search-page_main'})

    # Find the jobs table
    Jobtable = (start.table.tbody.findAll('tr'))

    for child in Jobtable:
        titleSource = child.find('td',attrs={'class':'esma_library-title'})
        jobCode = child.find('td',attrs={'class':'esma_library-ref'}).string
        jobLink = titleSource.a.get('href')
        jobTitle = titleSource.string
        jobDeadline = data_format.dateFormatFull(re.sub('\D','',jobTitle))
        jobType = data_format.typeOfGrade(jobCode)
        print (jobTitle, jobCode, jobLink,jobDeadline,jobType)
        esma.persist(int(esma_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)

    print("#========================ESMA SCRAPING COMPLETE=================================")

