import database as efsa
import urllib.request
from bs4 import BeautifulSoup


def scrapEFSA():

    print("#========================= EFSA SCRAPING =========================")

    # Database connection and agency retrieval

    efsaData = efsa.returnAgency('EFSA')
    efsa_link = efsaData['link'][0]
    efsa_id = efsaData['id'][0]

    html = urllib.request.urlopen(efsa_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.findAll('div',attrs={'class':'jlr_right_hldr'})



    for child in start:

        jobTitle = child.p.string
        jobLink = child.p.a.get('href')
        jobDept = child.find('div',attrs={'class':'jlr_content_half jlr_content_right'}).p.span.next_element.next_element.next_element.string
        print (jobTitle, jobLink,jobDept)
        efsa.persist(int(efsa_id), str(jobTitle).strip(), '', jobDept, '', 'SA', jobLink, '', 'Other')

    print("#======================== EFSA SCRAPING COMPLETE =================================")

