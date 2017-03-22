import re
import sqlite3
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

import persist


def scrapEPSO():

    print("#========================= EPSO SCRAPING =========================")
    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM eu_institute WHERE name="EPSO"''')
    epso_link = cur.fetchone()[7]
    html = urllib.request.urlopen(epso_link)
    text = html.read().decode('utf-8')
    soup = BeautifulSoup(text, "html.parser")

    def dateFormatFull (inputDate):
        dnotz = None
        for form in ['%d %b %Y', '%d %b %y',
        '%d %B %Y','%d/%m/%Y','%d.%m.%Y']:
            try:
                dnotz = datetime.strptime(inputDate, form).date()
                return str(dnotz)
            except:
                continue

        if dnotz is None :
            print ('Bad Date:',inputDate)
            return str(inputDate)

    start = soup.find(attrs={"class": "view-content"})
    page = 0
    while (start is not None):


        table = start.tbody.findAll("tr")

        for tr in table:
            #print (tr)
            print (tr.find(attrs={"class": "views-field views-field-field-epso-locations"}).get_text())
            print(tr.find(attrs={"class": "views-field views-field-title-field"}).get_text())
            institute= tr.find(attrs={"class": "views-field views-field-field-epso-institution-id"}).get_text()
            print(tr.find(attrs={"class": "views-field views-field-title-field"}).a.get("href"))
            dateFormatFull(tr.find(attrs={"class": "views-field views-field-field-epso-deadline"}).get_text())

            # Extract the agency code
            try:
                inst_code = re.search('\((.*?)\)', institute).groups()[0]
            except:
                inst_code = institute

            # Retrieve the agency's id from eu_institute
            try:
                cur.execute('''
                SELECT id FROM eu_institute WHERE name=?''', (inst_code,))
                inst_id = cur.fetchone()[0]
                print(inst_id)
            except:
                print("No information for agency/institution: " + inst_code)
                inst_id = 1

        page = int(page) + 1
        epso_link = epso_link + str(page)
        html = urllib.request.urlopen(epso_link)
        text = html.read().decode('utf-8')
        soup = BeautifulSoup(text, "html.parser")
        start = soup.find(attrs={"class": "view-content"})

    i = 2

    while (start is not None):

        # Look for the institution's title
        inst_title = start.next_sibling.next_sibling

        # Extract the agency code
        inst_code = re.search('\((.*?)\)', inst_title.string).groups()[0]

        # Retrieve the agency's id from eu_institute
        try:
            cur.execute('''
            SELECT id FROM eu_institute WHERE name=?''', (inst_code,))
            inst_id = cur.fetchone()[0]
        except:
            print ("No information for agency/institution: " + inst_code)
            inst_id = 1
        # Look for the ad
        postItem = inst_title.next_sibling.next_sibling

        while postItem.has_attr('class') is not True:

            # Construct the ad text for the raw database
            ad_raw = grade = deadline = ''

            for piece in postItem.contents:
                try:
                    url = piece.find('a').get('href')
                except:
                    pass

                try:

                    for item in piece.find_all('br'):
                        info = str(item.contents).split('<br>')
                        for infopiece in info:
                            infopiece = re.sub('<[^<]+?>', '',infopiece)
                            infopiece.strip()
                            if infopiece.startswith("Deadline"):# or "deadline" in infopiece.strip():
                                try:

                                    item_deadline = infopiece.split (":")[1].strip()

                                    deadline = dateFormatFull(item_deadline)

                                except:

                                    pass




                            elif (re.sub('[^A-Za-z0-9]+', '', infopiece).strip().startswith("Grade")):
                                print (re.sub('[^A-Za-z0-9]+', '', infopiece))
                                grade = infopiece.split (":")[1]

                            else:
                                continue
                except:
                    #grade = deadline = ''
                    pass

                ad_raw = ad_raw + str(piece).strip()

                if re.search('(AD+\d{1,2}?|AD +\d{1,2}?)',ad_raw) is not None:
                    jobType="AD"
                elif re.search('(AST+\d{1,2}?|AST +\d{1,2}?)',ad_raw)is not None:
                    jobType="AST"
                elif re.search('(FG+\d|FG+III|FG+IV|Function Groups)',ad_raw)is not None:
                    jobType="CA"
                elif re.search('(trainee)',ad_raw,re.IGNORECASE)is not None:
                    jobType="Trainee"
                elif re.search('(SNE|Seconded)',ad_raw,re.IGNORECASE)is not None:
                    jobType="SNE"
                else:
                    jobType="Other"



            # Insert job details in database
            #persist.dbpers(inst_id, '', str(grade).strip(), '', '', deadline, str(url).strip(), ad_raw, jobType)


            # Go to the next probable ad for the same institute
            postItem = postItem.next_sibling.next_sibling


        # Print agency code and name and re-enter loop
        print(inst_code, '\n', inst_title.string)
        start = soup.find(attrs={"name": "chapter" + str(i)})
        i = i + 1





    print("#========================EPSO SCRAPING COMPLETE=================================")

scrapEPSO()