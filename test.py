'''SELECT eu_institute.name as institute, COUNT (DISTINCT eu_job.job_id) as totals FROM eu_job, \
eu_institute WHERE eu_institute.id = eu_job.eu_institute_id GROUP BY institute ORDER BY totals desc'''


from datetime import datetime

def dateFormatting (inputDate):
    dnotz = None
    for form in ['%d %b %Y', '%d %b %y',
        '%d %B %Y','%d/%m/%Y']:
        try:
            dnotz = datetime.strptime(inputDate, form).date()
            return str(dnotz)
        except:
            continue

    if dnotz is None :
        print ('Bad Date:',inputDate)
        return str(inputDate)


def dateFormat (inputDate):
    date_object = datetime.strptime(inputDate, '%d/%m/%Y')
    return date_object.date()

    try:
        date_object = datetime.strptime(inputDate, '%d %B %Y')
        return date_object.date()

    except:
        date_object = datetime.strptime(inputDate, '%d %b %Y')
        return date_object.date()

    finally:
        print ("could not modify date " + inputDate)
        return inputDate

#print (date_object.date())
   # else:

print(dateFormatting('30 April 2016'))