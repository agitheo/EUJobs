import re
import database as epso
import urllib.request
import data_format
from bs4 import BeautifulSoup





def scrapEPSO():

    print("#========================= EPSO SCRAPING =========================")

    epsoData = epso.returnAgency('EPSO')
    epso_link = epsoData['link'][0]

    html = urllib.request.urlopen(epso_link)
    text = html.read().decode('utf-8')
    soup = BeautifulSoup(text, "html.parser")

    #Initiate scrap
    start = soup.find(attrs={"class": "view-content"})
    page = 0

    while (start is not None):
        table = start.tbody.findAll("tr")
        for tr in table:
            # Retrieve job information
            print (tr.find(attrs={"class": "views-field views-field-field-epso-locations"}).get_text())
            jobTitle = tr.find(attrs={"class": "views-field views-field-title-field"}).get_text()
            grade = tr.find(attrs={"class": "views-field views-field-field-epso-grade"}).get_text()
            institute = tr.find(attrs={"class": "views-field views-field-field-epso-institution-id"}).get_text()
            url = "https://epso.europa.eu"+ tr.find(attrs={"class": "views-field views-field-title-field"}).a.get("href")
            date_deadline = tr.find(attrs={"class": "views-field views-field-field-epso-deadline"}).get_text()
            contract = tr.find(attrs={"class": "views-field views-field-field-epso-type-of-contract"}).get_text()
            deadline = data_format.dateFormatFull(date_deadline.split ("-")[0].strip())

            # Extract the agency code
            try:
                inst_code = re.search('\((.*?)\)', institute).groups()[0]
            except:
                inst_code = institute

            check_institute = epso.EPSOinstitution(inst_code)

            #print ("inst:" + check_institute)

            if check_institute[2] == 1:
                continue

            # Retrieve the agency's id from eu_institute
            inst_id = check_institute[0]

            # Retrieve the agency's type from eu_institute
            inst_type = check_institute[1]

            # Determine the grade
            jobType = data_format.typeOfGrade(grade)


            # Insert job details in database
            epso.persist(inst_id, jobTitle, str(grade).strip(), str(institute).strip(), '', deadline, str(url).strip(), inst_type, jobType)
            print (inst_id, jobTitle, str(grade).strip(), str(institute).strip(), '', deadline, str(url).strip(), inst_type, jobType)

        page = int(page) + 1
        epso_link = epso_link + str(page)
        html = urllib.request.urlopen(epso_link)
        text = html.read().decode('utf-8')
        soup = BeautifulSoup(text, "html.parser")
        start = soup.find(attrs={"class": "view-content"})

        i = 2
    print("#========================EPSO SCRAPING COMPLETE=================================")

