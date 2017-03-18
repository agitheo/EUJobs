from datetime import datetime

def dateFormat (inputDate):

    try:
        date_object = datetime.strptime(inputDate, '%d %B %Y')
        return date_object.date()

    except:
        print ("could not modify date " + inputDate)
        return inputDate

    try:
        date_object = datetime.strptime(inputDate, '%d %b %Y')
        return date_object.date()

    except:
        print ("could not modify date " + inputDate)
        return inputDate

    else:
        date_object = datetime.strptime(inputDate, '%d/%m/%Y')
        return date_object.date()



#print (date_object.date())