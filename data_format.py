import re
from datetime import datetime


def dateFormatFull(inputDate):
    if (inputDate == ''):
        return 'n/a'
    elif (inputDate == 'SA'):
        return 'See Announcement'
    dnotz = None
    for form in ['%d %b %Y', '%d %b %y', '%d %m %Y',
                 '%d %B %Y', '%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y', '%d%m%Y', '%Y-%m-%d']:
        try:
            dnotz = datetime.strptime(inputDate, form).date()
            #return str(dnotz)
            return dnotz
        except:
            continue

    if dnotz is None:
        print('Bad Date:', inputDate)
        return str(inputDate)



def typeOfPost (type):
    if re.search('Permanent', type) or re.search('Official', type) :
        post = 'EU Off'
    elif re.search('Temporary', type) or re.search('AD', type):
        post = 'TA'
    elif re.search('Contract', type):
        post = 'CA'
    elif re.search('SNE', type):
        post = 'SNE'
    else:
        post = 'OTHER'
    return post

def typeOfGrade (grade):
    if re.search('(AD+\d{1,2}?|AD +\d{1,2}?)', grade) is not None:
        jobType = "AD"
    elif re.search('(AST+\d{1,2}?|AST +\d{1,2}?)', grade) is not None:
        jobType = "AST"
    elif re.search('(FG+\d|FG+III|FG+IV|Function Groups)', grade) is not None:
        jobType = "CA"
    elif re.search('(trainee)', grade, re.IGNORECASE) is not None:
        jobType = "Trainee"
    elif re.search('(SNE|Seconded)', grade, re.IGNORECASE) is not None:
        jobType = "SNE"
    else:
        jobType = "Other"
    return jobType