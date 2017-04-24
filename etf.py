import database as etf
import urllib.request
from bs4 import BeautifulSoup
import data_format

def scrapETF():

    print("#========================= ETF SCRAPING =========================")

    # Database connection and agency retrieval

    etfData = etf.returnAgency('ETF')
    etf_link = etfData['link'][0]
    etf_id = etfData['id'][0]

    html = urllib.request.urlopen(etf_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.find('div',attrs={'class':'content_group piclist_content'})

    # Find the jobs table
    Jobtable = start.find('div').div.ul

    for child in Jobtable.children:

        jobTitle = child.div.h2.string
        jobLink = "http://www.etf.europa.eu" + child.div.p.a.get('href')
        jobCode = child.div.p.a.string
        jobDeadline = data_format.dateFormatFull(str(child.div.p)[12:22])
        print (jobTitle, jobLink.replace(' ','%20'), jobCode, jobDeadline)
        etf.persist(int(etf_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', 'Other')

    print("#======================== ETF SCRAPING COMPLETE =================================")