import database as eba
import urllib.request
import datetime
from bs4 import BeautifulSoup
import data_format
import re

def scrapEBA():
    print("#========================= EBA SCRAPING =========================")

    # Database connection and agency retrieval

    ebaData = eba.returnAgency('EBA')
    eba_link = ebaData['link'][0]
    eba_id = ebaData['id'][0]

    pages = {"CA": "contract-agents", "TA": "temporary-agents", "SNE": "national-experts-on-secondment"}

    for pairs in pages:
        title = pairs.title().upper()
        page_link = (eba_link + "/" + pages[title])


        html = urllib.request.urlopen(page_link)
        soup = BeautifulSoup(html, "html.parser")


        # Create the soup
        start = soup.find('table', attrs={'class': 'Tabular'})
        today = datetime.datetime.today().date()


        # Find the jobs table
        Jobtable = (start.findAll('tr'))

        for cell in Jobtable:

            td = cell.findAll('td')
            try:
                status = td[3].string.strip()
                rawDate = td[2].string
                searchDate = re.match(r'(.*)at', rawDate)
                date = data_format.dateFormatFull(searchDate.group(1).strip())
            except:
                continue

            if (today < date) and (status == "ongoing"):

                jobLink = eba_link[:24] + td[0].a.get('href')
                jobTitle = td[0].string
                jobCode = td[1].string.strip()
                jobDeadline = date
                jobType = title
                print(jobCode, jobTitle, jobType, jobDeadline, jobLink)
                eba.persist(int(eba_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)
            else:
                continue

    print("#========================EBA SCRAPING COMPLETE=================================")
