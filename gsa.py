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

        print(page_link)


        # Create the soup
        start = soup.find(attrs='views-table cols-5 table table-striped table-bordered table-0 table-0')
        today = datetime.datetime.today().date()

        realStart = str(start).strip('</p>')


        # Find the jobs table
        #Jobtable = (realStart.findAll ('tr'))

        print(realStart)
'''
        for cell in Jobtable:
            jobCodeLocation = cell.td
            jobTitleLocation = jobCodeLocation.next_sibling
            print (jobCodeLocation.string,jobTitleLocation)

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