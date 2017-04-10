import database as satcen
import json
import urllib.request
from bs4 import BeautifulSoup
import data_format as format

def scrapSatCen():

    print("#========================= SatCen SCRAPING =========================")

    SatCenData = satcen.returnAgency('SATCEN')
    SatCen_link = SatCenData['link'][0]
    SatCen_id = SatCenData['id'][0]
    SatCen_source = urllib.request.urlopen(SatCen_link)

#Retrieve the list of jobs as bs4 navigable string
    soup = BeautifulSoup(SatCen_source,'html.parser')



        #Convert to bytes
    bytesEncoded = soup.encode('utf-8')
#Convert to string
    stringDecoded = bytesEncoded.decode('utf-8')
#Convert to dictionary
    jobsdict = json.loads(stringDecoded)
#Browse dictionaty and select available positions
    for job in jobsdict:
        if (job['Status']=='OPEN') and (job['InternalOnly'] == False):
            link = 'https://apps.satcen.europa.eu/recruitment/#/vacancy/'+job['Id']
            print(job['Reference'], job['ExpireOn'][:10],job['Title'],format.typeOfPost(job['TypePost']),job['WorkUnit'],link)
            satcen.persist(SatCen_id, job['Title'],job['Reference'],job['WorkUnit'],'', job['ExpireOn'][:10],link,'', format.typeOfPost(job['TypePost']))

    print("#========================SATCEN SCRAPING COMPLETE=================================")


