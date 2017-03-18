import re
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

import persist


def scrapEUROPOL():

    print("#========================= EUROPOL SCRAPING =========================")
    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM eu_institute WHERE name="EUROPOL"''')
    europol_q = cur.fetchone()
    europol_link = europol_q[7]
    europol_id = europol_q[0]

    html = urllib.request.urlopen(europol_link)
    soup = BeautifulSoup(html, "html.parser")

    # Find the first ad
    start = soup.findAll(attrs={"class":"views-table cols-6"})


    # Iterate through the tables
    for table in start:
        for ad in table.findAll("tr"):#,attrs={"class":"views-field views-field-field-vacancy-department-value"}):
            try:
                titleLink = ad.find ('td',attrs={"class":"views-field views-field-title"})
                title = titleLink.get_text()
                url = titleLink.find('a').get('href')
                dept = ad.find ('td',attrs={"class":"views-field views-field-field-vacancy-unit-value"}).get_text() + \
                       ad.find ('td',attrs={"class":"views-field views-field-field-vacancy-department-value"}).get_text().strip()
                jobTitle = ad.find ('td',attrs={"class":"views-field views-field-field-vacancy-post-value"}).get_text()
                deadline = ad.find ('td',attrs={"class":"views-field views-field-field-vacancy-deadline-value"}).get_text().strip()

                print (jobTitle.strip(),deadline.strip())
            except:
                continue

            try:
                date_object = datetime.strptime(deadline, '%d/%m/%Y')
                deadline = date_object.date()
            except:
                print ("could not modify " + deadline)
                pass

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

            persist.dbpers(int(europol_id), str(jobTitle).strip(), '', str(dept).strip(), str(title).strip(), deadline, str(url).strip(), '', jobType)

    print("#========================EUROPOL SCRAPING COMPLETE=================================")

