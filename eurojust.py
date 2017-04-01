import database
import re
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime



def scrapEurojust():

    print("#========================= EUROJUST SCRAPING =========================")

    # Database connection and agency retrieval
    eurojust = database.dataBase()
    eurojustData = eurojust.returnAgency('EUROJUST')
    eurojust_link = eurojustData['link'][0]
    eurojust_id = eurojustData['id'][0]



    html = urllib.request.urlopen(eurojust_link)
    soup = BeautifulSoup(html, "html.parser")


    def dateFormatFull (inputDate):

        dnotz = None
        for form in ['%d/%m/%Y', '%d %m %Y', '%d %b %Y', '%d %b %y',
        '%d %B %Y','%d.%m.%Y','%m/%d/%Y','%x']:
            try:
                dnotz = datetime.strptime(inputDate.strip(), form).date()
                return str(dnotz)
            except:
                continue

        if dnotz is None :
            print ('Bad Date:',inputDate)
            return str(inputDate)

    # Find the first ad
    start = soup.findAll("table",attrs={"class":"vacancyAnnouncements2"})


    # Iterate through the tables
    for table in start:
        for ad in table.findAll("tr",attrs={"class":"vacancyAnnouncements2Row" or "vacancyAnnouncements2AlternatingRow"}):
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
                    deadlineFormatted = dateFormatFull(str(deadline).replace('/',' '))
                    continue
                else:
                    pass

                print (jobTitle, deadlineFormatted)
                if re.search('(AD+\d{1,2}?|AD +\d{1,2}?|TA)',title) is not None:
                    jobType="AD"
                elif re.search('(AST+\d{1,2}?|AST +\d{1,2}?)',title)is not None:
                    jobType="AST"
                elif re.search('(FG+\d|FG+III|FG+IV|Function Groups|CA)',title)is not None:
                    jobType="CA"
                elif re.search('(trainee)',title,re.IGNORECASE)is not None:
                    jobType="Trainee"
                elif re.search('(SNE|Seconded)',title,re.IGNORECASE)is not None:
                    jobType="SNE"
                else:
                    jobType="Other"

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
                    deadline = piece.get_text().strip()
                    deadlineFormatted = dateFormatFull(deadline)
                    continue
                else:
                    pass
            print (jobTitle, deadline)
            '''try:
                date_object = datetime.strptime(str(deadline.strip), '%d/%m/%Y')
                deadline = date_object.date()
                return deadline
            except:
                pass
'''
            if re.search('(AD+\d{1,2}?|AD +\d{1,2}?|TA)',title) is not None:
                jobType="AD"
            elif re.search('(AST+\d{1,2}?|AST +\d{1,2}?)',title)is not None:
                jobType="AST"
            elif re.search('(FG+\d|FG+III|FG+IV|Function Groups|CA)',title)is not None:
                jobType="CA"
            elif re.search('(trainee)',title,re.IGNORECASE)is not None:
                jobType="Trainee"
            elif re.search('(SNE|Seconded)',title,re.IGNORECASE)is not None:
                jobType="SNE"
            else:
                jobType="Other"

            # Insert job details in database
            eurojust.persist(int(eurojust_id), str(jobTitle).strip(), '', '', str(title).strip(), deadlineFormatted, str(url).strip(), '', jobType)
    print("#========================EUROJUST SCRAPING COMPLETE=================================")

scrapEurojust()