#agencies = ['eda']

import database
import threading
import logging

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
import bbi
import eba
import cdt
import eacea
import etf

database.clean()

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )


epsoThread = threading.Thread(target=epso.scrapEPSO)

eupolThread = threading.Thread(target=eupol.scrapEUROPOL)

eujustThread = threading.Thread(target= eurojust.scrapEurojust)

emsaThread = threading.Thread(target=emsa.scrapEMSA)

f4eThread = threading.Thread(target=f4e.scrapF4E)

edaThread = threading.Thread(target=eda.scrapEDA)

satcenThread = threading.Thread(target=satcen.scrapSatCen)

emaThread = threading.Thread(target=ema.scrapEMA)

cpvoThread = threading.Thread(target=cpvo.scrapCPVO)

esmaThread = threading.Thread(target=esma.scrapESMA)

bbiThread = threading.Thread(target=bbi.scrapBBI)

ebaThread = threading.Thread(target=eba.scrapEBA)

cdtThread = threading.Thread(target=cdt.scrapCDT)

eaceaThread = threading.Thread(target=eacea.scrapEACEA)

etfThread = threading.Thread(target=etf.scrapETF)

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
bbiThread.start()
ebaThread.start()
cdtThread.start()
eaceaThread.start()
etfThread.start()