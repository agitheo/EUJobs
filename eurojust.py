import database as eurojust
import re
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import data_format

def scrapEurojust():

    print("#========================= EUROJUST SCRAPING =========================")

    # Database connection and agency retrieval

    eurojustData = eurojust.returnAgency('EUROJUST')
    eurojust_link = eurojustData['link'][0]
    eurojust_id = eurojustData['id'][0]

    html = urllib.request.urlopen(eurojust_link)
    soup = BeautifulSoup(html, "html.parser")

    # Find the first ad
    start = soup.findAll("table",attrs={"class":"vacancyAnnouncements2"})


    # Iterate through the tables
    for table in start:
        for ad in table.findAll("tr",attrs={"class":"vacancyAnnouncements2Row"}):
            title = jobType = deadline = url = jobTitle = None

            for piece in ad.findAll("td"):
                if (title is None):
                    title = piece.get_text()
                    continue
                elif (url is None):
                    url = piece.find('a').get('href')
                    jobTitle = piece.get_text()
                    continue
                elif (deadline is None):
                    deadline = piece.get_text()[1:]
                    deadlineFormatted = data_format.dateFormatFull(str(deadline).replace('/',' '))
                    continue
                else:
                    pass

                print (jobTitle, deadlineFormatted)
                jobType = data_format.typeOfGrade(title)

                eurojust.persist(int(eurojust_id), str(jobTitle).strip(), '', '', str(title).strip(), deadlineFormatted, str(url).strip(), '', jobType)


        for ad in table.findAll("tr",attrs={"class" : "vacancyAnnouncements2AlternatingRow"}):
            title = deadline = url = jobTitle = jobType = None

            for piece in ad.findAll("td"):
                if (title is None):
                    title = piece.get_text()
                    continue
                elif (url is None):
                    url = piece.find('a').get('href')
                    jobTitle = piece.get_text()
                    continue
                elif (deadline is None):
                    deadline = piece.get_text()[1:]
                    deadlineFormatted = data_format.dateFormatFull(str(deadline).replace('/', ' '))
                    continue

                else:
                    pass
            print (jobTitle, deadlineFormatted)

            jobType = data_format.typeOfPost(title)

            # Insert job details in database
            eurojust.persist(int(eurojust_id), str(jobTitle).strip(), '', '', str(title).strip(), deadlineFormatted, str(url).strip(), '', jobType)

    print("#========================EUROJUST SCRAPING COMPLETE=================================")

