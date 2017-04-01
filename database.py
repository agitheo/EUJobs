import sqlite3
from collections import OrderedDict

class dataBase:
    'Class to handle database connection, retrieval and commits'

    cur=''
    conn=''

    def __init__(self):
        dataBase.conn = sqlite3.connect('euJobs.sqlite')
        dataBase.cur = dataBase.conn.cursor()


    def returnAgency (self,agency):
        dataBase.cur.execute('''
                    SELECT * FROM eu_institute WHERE name=?''', (agency,))
        result = dataBase.cur.fetchone()
        keys = ['id','codeName','country','city','address','fullName','type','link','extraCode']
        agencyList = OrderedDict(zip(keys, zip(result)))
        return agencyList

    def persist(self,inst_id, title, grade, dept, desc, deadline, url, ad_raw, type):

        sql = 'INSERT INTO eu_job (eu_institute_id, title, grade, department, description, deadline, link, other,type)' \
              ' VALUES(?,?,?,?,?,?,?,?,?)'
        dataBase.cur.execute(sql,
                     (inst_id, title, grade, dept, desc, deadline, str(url).strip(), ad_raw, type,))
        dataBase.conn.commit()



