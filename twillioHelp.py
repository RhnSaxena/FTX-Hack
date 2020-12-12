from twilio.rest import Client
from urlpath import URL
import requests
import time
import csv
import personal_config
import config
import create_payment_link as pl
import pymongo
import json

account = personal_config.SID
token = personal_config.AUTH_TOKEN

def DownloadFile(url, unique, dir):
    r = requests.get(url)
    headers = r.headers
    ctype = headers['Content-Type'].split("/")[0]
    filename = str(time.time())
    with open(dir+unique+filename + ".csv", "wb") as f:
        f.write(r.content)
    return unique+filename

def sendSMS(client, from_, to_, msg):
    try:
        client.messages.create(body=msg, from_=from_, to=to_)
        return True
    except:
        return False

def readCSV(dir, filename,teacher_account_id, originalFileName, from_, db, sheets):
    try:
        arr = []
        with open(dir + filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(row)
                    amount = int(row[3])
                    student = {
                        "name":row[0],
                        "contact" : "+91"+row[1],
                        "email":row[2]
                    }
                    response = pl.create_link(student,amount, teacher_account_id, line_count-1,originalFileName)
                    print(amount)
                    print("------------------------------------")
                    response = json.loads(response)
                    print(response)
                    print("-------------------------------------")
                    student = {
                        "name":row[0],
                        "contact" : "+91"+row[1],
                        "email":row[2],
                        'amount': amount,
                        'TransactionId': response['id'],
                        'status': 'unpaid'
                    }
                    print(student)
                    arr.append(student)
                    line_count += 1
            print(f'Processed {line_count} lines.')
            sheets[originalFileName] = arr
            db.update_one({'user':from_}, {'$set': {'sheets': sheets}})
            return True
    except:
        return False

if __name__ == "__main__":
    # url = "https://api.twilio.com/2010-04-01/Accounts/ACee88cc6b6cf96910936801fa3726ccb5/Messages/MM2fb4f534d37e75bc93ec1daad6699373/Media/MEe5fe52624fc4d3e98e8439a14fb1625d";
    # DownloadFile(url,"unique","files/")
    # to_="whatsapp:+14155238886"
    # from_="whatsapp:+918604074906"
    # client = Client(account, token)
    # print(sendSMS(client, to_, from_, "Siddharth"))
    readCSV("files/","unique1607688708.30055.csv")
    # clientdb = pymongo.MongoClient("mongodb+srv://root:root@cluster0.g2z5c.mongodb.net")
    # db = clientdb.ftx.user
    # print(db)
    # ans = db.find_one({'user':"whatsapp:+918604074906"})
    # ans['sheets']['new'] = "sid"
    # print(ans['sheets'])
    # db.update_one({'user':"whatsapp:+918604074906"}, {'$set': {'sheets': ans['sheets']}})
