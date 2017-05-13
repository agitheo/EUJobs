import sqlite3
from collections import OrderedDict



def returnAgency (agency):

    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()

    cur.execute('''
                SELECT * FROM eu_institute WHERE name=?''', (agency,))
    result = cur.fetchone()
    keys = ['id','codeName','country','city','address','fullName','type','link','extraCode']
    agencyList = OrderedDict(zip(keys, zip(result)))
    return agencyList

def persist(inst_id, title, grade, dept, desc, deadline, url, ad_raw, type):

    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()


    sql = 'INSERT INTO eu_job (eu_institute_id, title, grade, department, description, deadline, link, other,type)' \
              ' VALUES(?,?,?,?,?,?,?,?,?)'
    cur.execute(sql,
                     (inst_id, title, grade, dept, desc, deadline, str(url).strip(), ad_raw, type,))
    conn.commit()


def clean():

    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()


    cur.execute('''DELETE FROM "main"."eu_job"''')
    conn.commit()


def EPSOinstitution(inst_code):

    conn = sqlite3.connect('euJobs.sqlite')
    cur = conn.cursor()

    try:
        cur.execute('''
        SELECT id,checkType FROM eu_institute WHERE name=?''', (inst_code,))
        results = cur.fetchone()
        inst_id = results[0]
        check = results[1]
        #print(inst_id,check)#, checkType)
        other = 'EPSO'
        return inst_id, other, check
    except:
        print("No information for agency/institution: " + str(inst_code).strip())
        inst_id = 1
        other = 'EPSO'
        check = 2
        return inst_id, other, check
#print (EPSOinstitution('EFSA')[2])
