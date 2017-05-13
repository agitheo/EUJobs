import database as cdt
import urllib.request
from bs4 import BeautifulSoup
import data_format


def scrapCDT():

    print("#========================= CDT SCRAPING =========================")

    # Database connection and agency retrieval

    cdtData = cdt.returnAgency('CDT')
    cdt_link = cdtData['link'][0]
    cdt_id = cdtData['id'][0]

    html = urllib.request.urlopen(cdt_link)
    soup = BeautifulSoup(html, "html.parser")

    # Create the soup
    start = soup.findAll('div',attrs={'class':'ms-rtestate-read ms-rte-wpbox'})

    #print (start[1])#.ul.li.p.div.span.font.string.strip())

    for child in start:

        jobTitle = child.span.attrs['title']
        postType = jobTitle[:9].strip()
        for post in child.ul:
            try:
                #print (child.ul)
                job = post.find('h3')
                jobCode = job.a.string.strip()
                jobLink = "http://cdt.europa.eu" + job.a.get('href').replace(' ','%20')
                jobTitle = post.find('p').div.span.font.string.strip()
                jobType = data_format.typeOfPost(postType)
                jobDeadline = data_format.dateFormatFull('SA')
                print (jobCode,jobLink,jobTitle,jobType,jobDeadline)
                cdt.persist(int(cdt_id), str(jobTitle).strip(), '', '', jobCode, jobDeadline, jobLink, '', jobType)
            except: continue
    print("#========================CDT SCRAPING COMPLETE=================================")
