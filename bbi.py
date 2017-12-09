import database as bbi
import urllib.request
from bs4 import BeautifulSoup
import data_format



def scrapBBI():

    print("#========================= BBI SCRAPING =========================")

    # Database connection and agency retrieval

    bbiData = bbi.returnAgency('BBI')
    bbi_link = bbiData['link'][0]
    bbi_id = bbiData['id'][0]

    html = urllib.request.urlopen(bbi_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('tbody',attrs={'class':'ui-datatable-data ui-widget-content'})

    # Find the jobs table
    Jobtable = (start.findAll('tr'))

    for child in Jobtable:
        jobCodeLocation = child.td.next_sibling
        jobTitleLocation = jobCodeLocation.next_sibling
        jobTypeLocation = jobTitleLocation.next_sibling
        jobGradeLocation = jobTypeLocation.next_sibling
        jobDeadlineLocation = jobGradeLocation.next_sibling
        jobLinkLocation = jobDeadlineLocation.next_sibling

        jobCode = jobCodeLocation.string
        jobTitle = jobTitleLocation.string
        jobType = data_format.typeOfPost(jobTypeLocation.string)
        jobGrade = data_format.typeOfGrade(jobGradeLocation.string)
        jobDeadline = data_format.dateFormatFull(jobDeadlineLocation.string[:10])
        jobLink = jobLinkLocation.a.get('href')

        print (jobCode,jobTitle,jobType,jobGrade,jobDeadline,jobLink)

        bbi.persist(int(bbi_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)

    print("#========================BBI SCRAPING COMPLETE=================================")

scrapBBI()