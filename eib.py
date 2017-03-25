import sqlite3
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

import persist


def scrapEIB():

    print("#========================= EUROPEAN INVESTMENT BANK SCRAPING =========================")
    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM eu_institute WHERE name="EIB"''')
    eib_q = cur.fetchone()
    eib_link = eib_q[7]
    eib_id = eib_q[0]


    values = {'FOCUS':'Applicant','SiteId':'1','PortalActualURL':'https://erecruitment.eib.org/psc/hr/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL',\
          'PortalContentURL':'https://erecruitment.eib.org/psc/hr/EMPLOYEE/HRMS/c/HRS_HRAM.HRS_APP_SCHJOB.GBL','PortalContentProvider':'HRMS',\
          'PortalCRefLabel':'Current%20Vacancies%20-%20EIB%20Group','PortalRegistryName':'EMPLOYEE','PortalServletURI':'https://erecruitment.eib.org/psp/hr/',\
          'PortalURI':'https://erecruitment.eib.org/psc/hr/','PortalHostNode':'HRMS','NoCrumbs':'yes2016'}
    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    headers = { 'User-Agent' : user_agent }

    req = urllib.request.Request(eib_link,data,headers)

    with urllib.request.urlopen(req) as response:
        html = response.read()

    finalUrl = req.get_full_url()

    #full_link = eib_link + str(data)


    soup = BeautifulSoup(html, "html.parser")



    # Find the first ad
    start = soup.findAll(attrs={"class":"PSLEVEL1GRIDNBO"})

    # Retrieve text based on div id
    def drill(divId):
        element = ad.find ('div',attrs={"id":divId})
        try:
            return element.text
        except:
            return None



    # Iterate through the table rows
    for table in start:
        row=0
        for ad in table.findAll("tr"):
            titleId = "win0divHRS_SCH_WRK_HRS_HTMLAREA$" + str(row)
            jobId = "win0divJOBNUMBER$" + str(row)
            deptId = "win0divJOB_FUNCTION2$" + str(row)
            deadlId = "win0divOPENED$" + str(row)
            whereId =  "win0divHRS_LOCATION_DESCR$" + str(row)
            busUnitId = "win0divBUS_UNIT_TBL_HR_DESCR$127$$" + str(row)




            jobTitle = drill(titleId)

            if jobTitle is not None:
                id =  drill(jobId)
                dept = drill(deptId)
                deadline = drill(deadlId)
                deadline = deadline.strip()
                where = drill(whereId)
                busUnit = drill(busUnitId)
                row = row + 1
                jobType = "Trainee" if "Trainee" in jobTitle else "Other"
                print (jobTitle,id,dept,deadline,where)
            else:
                continue

            try:
                date_object = datetime.strptime(deadline, '%m/%d/%Y')
                deadline = date_object.date()
            except:
                print("could not modify " + deadline)
                pass

            #persist.dbpers(int(eib_id), str(jobTitle).strip(), '', str(dept).strip(), '', str(deadline).strip(), finalUrl, where + " " + busUnit, jobType)



    print("#========================= EUROPEAN INVESTMENT BANK SCRAPING COMPLETE=========================")
