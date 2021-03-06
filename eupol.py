import re
import database as europol
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime




def scrapEUROPOL():

    print("#========================= EUROPOL SCRAPING =========================")

    europolData = europol.returnAgency('EUROPOL')


    europol_link = europolData['link'][0]
    europol_id = europolData['id'][0]

    html = urllib.request.urlopen(europol_link)
    soup = BeautifulSoup(html, "html.parser")

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

    # Find all ads

    start = soup.findAll(attrs={"class":re.compile("^views-row views-row-")})

    #print ("posts found " + str(len(start)))

    # Iterate through the divs
    for advert in start:
        try:
            deadline = advert.find(attrs={"class":"views-field views-field-deadline"}).findAll('span')[1].get_text()
            deadlineFormatted = dateFormatFull(deadline)
            print ("Deadline:",dateFormatFull(deadline))



            print("Contract Type:", advert.find(attrs={"class": "views-field views-field-contract-type"}).find('span').get_text())

            jobTitle = advert.find("a").get_text()
            print("Title:", jobTitle)

            dept = advert.find(attrs={"class": "views-field views-field-department"}).find('span').get_text()
            print("Department:", dept)

            title = advert.find(attrs={"class": "views-field views-field-reference-number"}).find('span').get_text()
            print("Reference Number:", title)

            url = "http://www.europol.europa.eu" + advert.find("a").get("href")
            print("Link:", url)

        except:

            continue




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

        print(int(europol_id), str(jobTitle).strip(), '', str(dept).strip(), str(title).strip(), deadlineFormatted, str(url).strip(), '', jobType)
        europol.persist(int(europol_id), str(jobTitle).strip(), '', str(dept).strip(), str(title).strip(), deadlineFormatted,str(url).strip(), '', jobType)


    '''for div in start.findAll(attrs={"class":"views-field views-field-department"}):
        titleLink = div.find('span', attrs={"class": "field-content"})
        print(titleLink)
        for classes in div.findAll("class"):#,attrs={"class":"views-field views-field-field-vacancy-department-value"}):
            try:

                titleLink = classes.find ('span',attrs={"class":"views-label views-label-deadline"})
                print (titleLink)
                title = titleLink.get_text()
                url = titleLink.find('a').get('href')
                dept = classes.find ('td',attrs={"class":"views-field views-field-field-vacancy-unit-value"}).get_text() + \
                classes.find ('td',attrs={"class":"views-field views-field-field-vacancy-department-value"}).get_text().strip()
                jobTitle = classes.find ('td',attrs={"class":"views-field views-field-field-vacancy-post-value"}).get_text()
                deadline = classes.find ('td',attrs={"class":"views-field views-field-field-vacancy-deadline-value"}).get_text().strip()

        #print (jobTitle.strip(),deadline.strip())
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
    '''
    print("#========================EUROPOL SCRAPING COMPLETE=================================")

