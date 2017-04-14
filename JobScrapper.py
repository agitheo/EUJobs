import database
import threading

import eda
import emsa
import epso
import eupol
import eurojust
import f4e
import satcen
import ema
import cpvo
import esma



database.clean()

epsoThread = threading.Thread(target=epso.scrapEPSO)
eupolThread = threading.Thread(target=eupol.scrapEUROPOL)
eujustThread = threading.Thread(target= eurojust.scrapEurojust)
emsaThread = threading.Thread(target=emsa.scrapEMSA)
f4eThread = threading.Thread(target=eda.scrapEDA)
edaThread = threading.Thread(target=f4e.scrapF4E)
satcenThread = threading.Thread(target=satcen.scrapSatCen)
emaThread = threading.Thread(target=ema.scrapEMA())
cpvoThread = threading.Thread(target=cpvo.scrapCPVO())
esmaThread = threading.Thread(target=esma.scrapESMA())

eujustThread.start()
epsoThread.start()
eupolThread.start()
emsaThread.start()
edaThread.start()
f4eThread.start()
satcenThread.start()
emaThread.start()
cpvoThread.start()
esmaThread.start()