import re
from datetime import datetime


def dateFormatFull(inputDate):
    dnotz = None
    for form in ['%d %b %Y', '%d %b %y',
                 '%d %B %Y', '%d/%m/%Y', '%d.%m.%Y']:
        try:
            dnotz = datetime.strptime(inputDate, form).date()
            return str(dnotz)
        except:
            continue

    if dnotz is None:
        print('Bad Date:', inputDate)
        return str(inputDate)



def typeOfPost (type):

    if re.search('Permanent', type):
        return 'EU Off'
    elif re.search('Temporary', type):
        return 'TA'
    elif re.search('Contract Agent', type):
        return 'CA'
    elif re.search('SNE', type):
        return 'SNE'
    else:
        return 'OTHER'
