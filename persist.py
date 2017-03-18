import sqlite3



# Insert job details in database

def dbpers(inst_id,title,grade,dept,desc,deadline,url,ad_raw,type):

    conn5 = sqlite3.connect('euJobs.sqlite')
    cur5 = conn5.cursor()
    sql = 'INSERT INTO eu_job (eu_institute_id, title, grade, department, description, deadline, link, other,type) VALUES(?,?,?,?,?,?,?,?,?)'
    cur5.execute (sql,
            (inst_id,title,grade,dept,desc,deadline,str(url).strip(),ad_raw,type,))
    conn5.commit()
