import database as eiopa
import urllib.request
from bs4 import BeautifulSoup
import data_format
import re

def scrapEIOPA():

    print("#========================= EIOPA SCRAPING =========================")

    # Database connection and agency retrieval

    eiopaData = eiopa.returnAgency('EIOPA')
    eiopa_link = eiopaData['link'][0]
    eiopa_id = eiopaData['id'][0]

    html = urllib.request.urlopen(eiopa_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('table',attrs={'class':'ms-rteTable-EIOPATable'})


    for tr in start.tbody:
        if str(tr['class'][0]) == "ms-rteTableHeaderRow-EIOPATable":
            continue

        jobTitle = tr.th.next_sibling.a.string
        jobLink = "https://eiopa.europa.eu/" + tr.th.next_sibling.a.get('href')
        jobCode = str(re.match(r'(.*?)%20', jobLink).group(1)[29:])
        jobType = data_format.typeOfPost(jobCode)
        deadlinePosition = tr.td.next_sibling

        if re.match('\w',jobTitle[0]) is None:
            jobTitle = jobTitle[1:len(jobTitle)]


        if (len(deadlinePosition.contents[0].string)>2):
            jobDeadline = deadlinePosition.contents[0].string
            jobDeadline = str(jobDeadline).strip()
            jobDeadline = data_format.dateFormatFull(jobDeadline[1:])

        else:
            extendedDeadlines = deadlinePosition.findAll('strong')
            newDeadline = extendedDeadlines[len(extendedDeadlines)-1].string
            newDeadline = str(newDeadline.split(':')[1]).strip()
            jobDeadline = data_format.dateFormatFull(newDeadline)


        print(jobTitle, jobCode, jobType,  jobDeadline)

        eiopa.persist(int(eiopa_id), jobTitle, '', '', jobCode, jobDeadline, jobLink, '', jobType)

    print("#========================EIOPA SCRAPING COMPLETE=================================")

#scrapEIOPA()