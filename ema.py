import database as ema
import urllib.request
from bs4 import BeautifulSoup
import data_format

def scrapEMA():

    print("#========================= EMA SCRAPING =========================")

    # Database connection and agency retrieval

    emaData = ema.returnAgency('EMA')
    ema_link = emaData['link'][0]
    ema_id = emaData['id'][0]

    html = urllib.request.urlopen(ema_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('div',attrs={'class':'main-col'})

    # Find the jobs table
    Jobtable = (start.find('table'))

    for child in Jobtable.children:
        if(child.find('td',attrs={'colspan':'top'})):
            continue
        jobTitle = child.td.string
        jobCode = child.td.next_sibling.string
        jobType = data_format.typeOfPost(jobCode)
        jobLink = "http://www.ema.europa.eu/ema/" + child.td.next_sibling.next_sibling.a.get('href')
        jobDeadline = data_format.dateFormatFull(child.td.next_sibling.next_sibling.next_sibling.string)
        print(jobTitle,jobCode,jobType,jobLink,jobDeadline)
        ema.persist(int(ema_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)

    print("#========================EMA SCRAPING COMPLETE=================================")
