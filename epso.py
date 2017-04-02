import re
import database as epso
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime




def scrapEPSO():

    print("#========================= EPSO SCRAPING =========================")

    epsoData = epso.returnAgency('EPSO')
    epso_link = epsoData['link'][0]

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
            jobTitle = tr.find(attrs={"class": "views-field views-field-title-field"}).get_text()
            grade = tr.find(attrs={"class": "views-field views-field-field-epso-grade"}).get_text()
            institute = tr.find(attrs={"class": "views-field views-field-field-epso-institution-id"}).get_text()
            url = "https://epso.europa.eu"+ tr.find(attrs={"class": "views-field views-field-title-field"}).a.get("href")
            date_deadline = tr.find(attrs={"class": "views-field views-field-field-epso-deadline"}).get_text()
            contract = tr.find(attrs={"class": "views-field views-field-field-epso-type-of-contract"}).get_text()
            deadline = dateFormatFull(date_deadline.split ("-")[0].strip())

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
                print("No information for agency/institution: " + str(inst_code).strip())
                inst_id = 1
            if re.search('(AD+\d{1,2}?|AD +\d{1,2}?)', grade) is not None:
                jobType = "AD"
            elif re.search('(AST+\d{1,2}?|AST +\d{1,2}?)', grade) is not None:
                jobType = "AST"
            elif re.search('(FG+\d|FG+III|FG+IV|Function Groups)', grade) is not None:
                jobType = "CA"
            elif re.search('(trainee)', grade, re.IGNORECASE) is not None:
                jobType = "Trainee"
            elif re.search('(SNE|Seconded)', grade, re.IGNORECASE) is not None:
                jobType = "SNE"
            else:
                jobType = "Other"

            # Insert job details in database
            epso.persist(1, jobTitle, str(grade).strip(), str(institute).strip(), '', deadline, str(url).strip(), '', jobType)

        page = int(page) + 1
        epso_link = epso_link + str(page)
        html = urllib.request.urlopen(epso_link)
        text = html.read().decode('utf-8')
        soup = BeautifulSoup(text, "html.parser")
        start = soup.find(attrs={"class": "view-content"})

        i = 2
    print("#========================EPSO SCRAPING COMPLETE=================================")
'''
        while (start is not None):

            # Look for the institution's title
            inst_title = start.next_sibling.next_sibling

            # Extract the agency code
            inst_code = re.search('\((.*?)\)', inst_title.string).groups()[0]

            # Retrieve the agency's id from eu_institute
            try:
                cur.execute(''
                SELECT id FROM eu_institute WHERE name=?'', (inst_code,))
                inst_id = cur.fetchone()[0]
            except:
                print ("No information for agency/institution: " + inst_code)
                inst_id = 1
'''




'''        # Look for the ad
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







            # Go to the next probable ad for the same institute
            postItem = postItem.next_sibling.next_sibling


        # Print agency code and name and re-enter loop
        print(inst_code, '\n', inst_title.string)
        start = soup.find(attrs={"name": "chapter" + str(i)})
        i = i + 1


'''
