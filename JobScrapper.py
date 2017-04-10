import database
import threading

import eda
#import eib
import emsa
import epso
import eupol
import eurojust
import f4e
import satcen



database.clean()

epsoThread = threading.Thread(target=epso.scrapEPSO)
eupolThread = threading.Thread(target=eupol.scrapEUROPOL)
eujustThread = threading.Thread(target= eurojust.scrapEurojust)
#eibThread = threading.Thread(target= eib.scrapEIB)
emsaThread = threading.Thread(target=emsa.scrapEMSA)
f4eThread = threading.Thread(target=eda.scrapEDA)
edaThread = threading.Thread(target=f4e.scrapF4E)
satcenThread = threading.Thread(target=satcen.scrapSatCen)

eujustThread.start()
epsoThread.start()
eupolThread.start()
#eibThread.start()
emsaThread.start()
edaThread.start()
f4eThread.start()
satcenThread.start()
