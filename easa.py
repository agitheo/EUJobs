import database as easa
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import data_format


def scrapEASA():

    print("#========================= EASA SCRAPING =========================")

    easaData = easa.returnAgency('EASA')
    easa_link = easaData['link'][0]
    easa_id = easaData['id'][0]

    print (easa_link)

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    accept_Encoding = "gzip, deflate, br"
    accept_Language = "en, es - ES;q = 0.9, es;q = 0.8, en - GB;q = 0.7"
    cache = "max-age = 0"
    connection = "keep - alive"
    cookie="__unam=7494d75-15b02cb5cdd-11554c2a-10; ajs_user_id=null; ajs_group_id=null; _ga=GA1.2.307152274.1482181762; ASP.NET_SessionId=rseh31pqwxavvibhcwfv3sv1; BIGipServerHTTP_HTTPS_traffic_https_ERECRUITMENT=654362634.47873.0000; TS0139eb98=0136584751f1a7c8a64bc3fe933a9499b6371644a7126a72ff986347955114c6b0774a0b56da8578550e9385e17ca1b073fe62984423cfab527ecbe90bd918476ae21167fc; TS01176eef=01365847510c9f804bf082685cc573cc5bd160b8369d75b391ab38da3ea14de8fb4be532af"
    host = "erecruitment.easa.europa.eu"
    upgrade="1"

    headers = { 'Accept': accept,'Accept-Encoding':accept_Encoding,'Accept-Language':accept_Language,'Cache-Control':cache,'Connection':connection , 'Cookie':cookie,'Host':host,'Upgrade-Insecure-Requests':upgrade,'User-Agent' : user_agent }
    data = ''
    data = data.encode('ascii')


    req = urllib.request.Request(easa_link,data,headers)



    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "html.parser")


    # Find the first ad
    start = soup.findAll(attrs={"class":"vacancyrow"})

    print (soup)
    print("#========================EASA SCRAPING COMPLETE=================================")

scrapEASA()

