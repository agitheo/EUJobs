import sqlite3
from datetime import datetime
import time
from datetime import datetime


conn = sqlite3.connect('euJobs.sqlite')
cur = conn.cursor()

cur.execute ('''SELECT eu_institute.description, eu_institute.country, eu_institute.address,
eu_job.title, eu_job.grade, eu_job.description, eu_job.deadline, eu_job.department , eu_job.link, eu_job.other, eu_job.type
FROM eu_institute, eu_job WHERE eu_institute.id=eu_job.eu_institute_id ORDER BY eu_job.deadline ASC''')

current_possitions = cur.fetchall()

cur.execute ('''SELECT COUNT (DISTINCT eu_institute.description) FROM eu_institute, eu_job WHERE \
 eu_institute.id=eu_job.eu_institute_id''')

intstNum = cur.fetchone()


html = open("index.html",'w')

html.write('<!DOCTYPE html> <html> <head> \
<meta name="viewport" content="width=device-width, initial-scale=1"> \
<link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css"> \
<script src="http://code.jquery.com/jquery-1.11.3.min.js"></script> \
<script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script> \
<style> \
th \
{ \
border-bottom: 1px solid #d6d6d6; \
} \
tr:nth-child(even) \
{ \
background:#e9e9e9; \
} \
</style> \
</head> \
<body> \
<div data-role="page" id="pageone"> \
  <div data-role="header"> \
    <h1><a href="linestats2.html" target="_blank">'+str(len(current_possitions))+' Posts available from '+ str(intstNum)[1:-2] +' EU institutions</a></h1> \
  </div> \
  <div data-role="main" class="ui-content"> \
    <form> \
      <input id="filterTable-input" data-type="search" placeholder="Search..."> \
    </form> \
    <table data-role="table" data-mode="columntoggle" class="ui-responsive ui-shadow" id="myTable" data-filter="true" data-input="#filterTable-input"> \
      <thead> \
        <tr> \
          <th data-priority="1">Institute</th> \
          <th data-priority="2">Country</th> \
          <th data-priority="3">City</th> \
          <th data-priority="4">Post</th> \
          <th data-priority="5">Grade</th> \
          <th data-priority="6">Department</th> \
          <th data-priority="7">Deadline</th> \
          <th data-priority="8">Link</th> \
          <th data-priority="9">Type</th> \
        </tr> \
      </thead> \
      <tbody> \
      ')


for position in current_possitions:
    str(position).encode('utf-8')
    html.write('<tr> <td>' + str(position[0])+ "</td>"+ "<td>" + str(position[1]) + "</td>" )
    html.write("<td>" + str(position[2]) + "</td>"+ "<td>" + str(position[3]) + " " + str(position[4]) + "</td>")
    html.write("<td>" + str(position[5]) + "</td>"+ "<td>" + str(position[7])+  "</td>")
    #html.write( "<td>" + str(position[6]).encode('utf-8') + "</td>" + "<td> <a href=" + position[7] + ">link</a></td>")
    html.write ("<td>" + str(position[6])+ "</td>")
    html.write( "<td> <a href="+ position[8] + "  target=_blank>link</a></td> <td>" + str(position[10]).strip('</br></tr>') + "</td>")



html.write (' </tbody> \
</table> \
</div> \
<div data-role="footer"> \
<h1>Footer Text</h1> \
</div> \
</div> \
</body> \
</html>\
')

html.close()

now = datetime.now().date()



cur.execute('''SELECT * FROM scraplog WHERE date_scrap = ?''', (now,))


if (cur.fetchone() is not None):

    cur.execute('''DELETE FROM scraplog WHERE date_scrap = ?''', (now,))
    conn.commit()


#cur.execute('''SELECT eu_institute.name as institute, eu_institute.id as instituteId, COUNT (DISTINCT eu_job.job_id) as totals FROM eu_job, \
#eu_institute WHERE eu_institute.id = eu_job.eu_institute_id GROUP BY institute ORDER BY totals desc''')

cur.execute('''SELECT eu_institute.name as institute,  eu_institute.id as instituteId, COUNT(eu_job.type) as totals, eu_job.type FROM eu_job, eu_institute \
WHERE eu_institute.id = eu_job.eu_institute_id GROUP BY eu_job.eu_institute_id, eu_job.type ORDER BY totals desc''')

adds_sum = cur.fetchall()

    #print (type(adds_sum), adds_sum)

for institute,instituteid,positions,type in adds_sum:
        #print (institute +" "+ str(instituteid) + " " + str(positions))
    sql = 'INSERT INTO scraplog (date_scrap, id_institute, totals,type) VALUES (?, ?, ?, ?)'
    cur.execute (sql,
        (str(now), instituteid, positions,type))
    conn.commit()

time.sleep(3)



cur.execute('''SELECT date_scrap, SUM(totals) FROM scraplog GROUP BY date_scrap''' )#WHERE date_scrap = ?''', (now,))
stats = cur.fetchall()

data1 = open("data1.csv",'w')

data1.write ("date,close\n")
for date, totals in stats:
    date_object = datetime.strptime(date, '%Y-%m-%d')
    data1.write (date_object.strftime('%d-%b-%y') + "," + str(float(totals))+"\n")

data1.close()

data2 = open("data2.csv",'w')


cur.execute('''SELECT date_scrap, COUNT (DISTINCT(id_institute)) as totals FROM scraplog GROUP BY date_scrap''' )
stats2 = cur.fetchall()
data2.write ("date,close\n")
for date, totals in stats2:
    date_object = datetime.strptime(date, '%Y-%m-%d')
    data2.write (date_object.strftime('%d-%b-%y') + "," + str(float(totals))+"\n")

data2.close()

data = open("data.csv",'w')


cur.execute('''SELECT date_scrap FROM scraplog ORDER BY date_scrap desc LIMIT 1''' )
latest_date = cur.fetchone()[0]

cur.execute('''SELECT eu_institute.name as institute, SUM(scraplog.totals) as posts  FROM  scraplog, eu_institute\
 WHERE eu_institute.id=scraplog.id_institute AND  scraplog.date_scrap=? GROUP BY id_institute ORDER BY posts DESC''', (latest_date,))

stats = cur.fetchall()
data.write ("age,population\n")
for institutes, posts in stats:
    data.write (institutes + "/" + str(int(posts)) + "," + str(float(posts))+"\n")

data.close()

#data3 = open("data.csv",'w')

cur.execute('''SELECT date_scrap, SUM(totals), type FROM scraplog WHERE type IS NOT NULL GROUP BY type,date_scrap ORDER BY date_scrap ASC''')
seriesType = cur.fetchall()
#data.write ("date,AD,CA,Other,SNE,Trainee\n")

startdate = seriesType[0][0]

#while
#for scrapDate in seriesType:
#    print (scrapDate[0])
    #data.write (seriesType[0]+","+seriesType[1]+","+seriesType[0]+","+
