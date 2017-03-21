import sqlite3
import threading
import time

import eda
import eib
import emsa
import epso
import eupol
import eurojust

conn = sqlite3.connect('euJobs.sqlite')
cur = conn.cursor()
cur.execute ('''DELETE FROM "main"."eu_job"''')
conn.commit()

#epsoThread = threading.Thread(target=epso.scrapEPSO)
eupolThread = threading.Thread(target=eupol.scrapEUROPOL)
eujustThread = threading.Thread(target= eurojust.scrapEurojust)
#eibThread = threading.Thread(target= eib.scrapEIB)
emsaThread = threading.Thread(target=emsa.scrapEMSA)
edaThread = threading.Thread(target=eda.scrapEDA)

eujustThread.start()
#epsoThread.start()
eupolThread.start()
#eibThread.start()
emsaThread.start()
edaThread.start()


