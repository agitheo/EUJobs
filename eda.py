import sqlite3
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime

import persist


def scrapEDA():

    print("#========================= EDA SCRAPING =========================")
    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM eu_institute WHERE name="EDA"''')
    eda_q = cur.fetchone()
    eda_link = eda_q[7]
    eda_id = eda_q[0]

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
    headers = { 'User-Agent' : user_agent }
    data = ''
    data = data.encode('ascii')


    req = urllib.request.Request(eda_link,data,headers)

    #print(emsa_link)

    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "html.parser")

    # Iterate through the internal groups
    for post_type in soup.find_all("h4"):

        internal_type = post_type.contents[0].strip()

        if internal_type not in ('Temporary Agents','Contractual Agents','Seconded National Experts'):
            continue
        elif internal_type == 'Temporary Agents':
            job_type = 'TA'
        elif internal_type == 'Contractual Agents':
            job_type = 'CA'
        else:
            job_type = 'SNE'

        print (post_type.contents[0])

        internals = post_type.next_element.next_element.next_element.find_all("li")

    #try:
        # Iterate the URLs for each TA post
        for post in internals:

            ta_link = eda_link + post.find('a').get("href")
            ta_req = urllib.request.Request(ta_link,data,headers)

            with urllib.request.urlopen(ta_req) as response:
                ta_html = response.read()

            ta_soup = BeautifulSoup(ta_html, "html.parser")

            #Link
            print (ta_link)

            #Post
            post_title = ta_soup.findAll(attrs={"id":"cphMain_VacNotice_LabPost"})[0].contents[0].strip()
            print (post_title)

            #Grade
            post_grade = ta_soup.findAll(attrs={"id":"cphMain_VacNotice_LabGrade"})[0].contents[0].strip()
            print (post_grade)

            #Deadline
            post_deadline = ta_soup.findAll(attrs={"id":"cphMain_VacNotice_LabPublicationDateEnd"})
            print (post_deadline[0].contents[0].strip()+ "\n")
            # Convert date
            try:
                date_object = datetime.strptime(post_deadline[0].contents[0].strip(), '%d %B %Y')
                deadline = date_object.date()
                #print (deadline)
            except:
                print ("could not modify " + str(post_deadline))
                pass

            # Insert job details in database
            persist.dbpers(int(eda_id), str(post_title).strip(), str(post_grade), '', '', deadline, str(ta_link).strip(), '', job_type)
    #except:
     #   pass


    print("#========================EDA SCRAPING COMPLETE=================================")
