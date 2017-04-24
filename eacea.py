import database as eacea
import urllib.request
from bs4 import BeautifulSoup
import data_format

def scrapEACEA():

    print("#========================= EACEA SCRAPING =========================")

    # Database connection and agency retrieval

    eaceaData = eacea.returnAgency('EACEA')
    eacea_link = eaceaData['link'][0]
    eacea_id = eaceaData['id'][0]

    html = urllib.request.urlopen(eacea_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('table',attrs={'class':'table table-striped table-hover views-table cols-4'})

    # Find the jobs table
    Jobtable = (start.find('tbody'))

    rows = Jobtable.findAll('tr')


    for posts in rows:
        columns = posts.children

        for tds in columns:
            try:
                status = tds.next_sibling.next_sibling.next_sibling.next_sibling.span.string
                if (status == 'Open'):
                    jobLink = "http://eacea.ec.europa.eu"+ tds.a.get('href')
                    jobTitle = tds.a.string
                    deadline = tds.next_sibling.next_sibling.span.string
                    jobDeadline = data_format.dateFormatFull(deadline[:10])
                    if jobTitle.find('CA-FG')> 0:
                        jobType = "CA"
                    else:
                        jobType = "Other"
                    print(jobTitle, jobLink, jobType, jobDeadline)
                    eacea.persist(int(eacea_id), str(jobTitle).strip(), '', '', '', jobDeadline, jobLink, '', jobType)
                else: continue
            except:
                continue

    print("#========================EACEA SCRAPING COMPLETE=================================")
