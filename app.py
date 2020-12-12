# from flask_pymongo import PyMongo
import pymongo
from twilio.rest import Client
from flask import Flask, request
import twillioHelp as tw
import report_link as rl
import personal_config
import requests
import config
import json

# App initialize
app = Flask(__name__)
clientdb = pymongo.MongoClient("mongodb+srv://root:root@cluster0.g2z5c.mongodb.net")
# clientdb = pymongo.MongoClient("mongodb://localhost:27017")
db = clientdb.ftx.user

account = personal_config.SID
token = personal_config.AUTH_TOKEN
client = Client(account, token)

# Welcome Endpoint
@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome To Manage Money API'

# End Point to connect with Twillio for WhatsApp
@app.route('/receive', methods=['POST'])
def receive():

    from_ = request.form['From']
    to_ = request.form['To']
    body = request.form['Body']
    NumMedia = request.form['NumMedia']
    Media = None

    print(request.form)
    if NumMedia != '0':
        Media = request.form['MediaUrl0']
        print(Media)
        tw.sendSMS(client, to_, from_, "Thank you for uploading file . we are processing it")
        file_name = tw.DownloadFile(Media, from_, "files/")
        teacherData = db.find_one({"user": from_})
        tw.readCSV("files/",file_name+".csv",teacherData['accountId'],body, from_, db, teacherData['sheets'])
        tw.sendSMS(client, to_, from_, "we have created the payment links, the customers will receive them soon.")
    
    else:
        try:
            if body[0] == "/":
                command = body.split(" ")
                ctype = command[0]
                if len(command) > 1:
                    anytext = command[1]
                    if ctype.lower() == "/greet":
                        tw.sendSMS(client, to_, from_, "HI "+ anytext)
                    if ctype.lower() == "/report":
                        #  call the report generate function with user id , sheet_name ,paid/unpaid
                        # ans = rl.report_link(db,"whatsapp:+918604074906","file1","unpaid")
                        ans = rl.report_link(db,from_,command[1],command[2])
                        ans = "Here you go,\n{}".format(ans)
                        tw.sendSMS(client, to_, from_, str(ans))
                else:
                    if ctype.lower()  == "/game":
                        tw.sendSMS(client, to_, from_, "i will play with you")
            else:
                print("I did not understand")
        except Exception as err:
            print(err)
            tw.sendSMS(client, to_, from_, "Error occured")
    return 'Receive'

@app.route('/callback', methods=['POST', 'GET'])
def callback():
    captureObject = request.get_json()
    print(captureObject["event"])
    if captureObject["event"] == "payment_link.paid":

        accountId="acc_GBihjkqRxFr1f6"
        url = "https://api.razorpay.com/v1/payments/{}/transfers/".format(captureObject["payload"]["payment"]["entity"]["id"])
        
        notes = captureObject["payload"]["order"]["entity"]['notes']
        payload=  {
            "transfers": [
                {
                "account":notes['teacher_account_id'],
                "amount": captureObject["payload"]["payment"]["entity"]["amount"],
                "currency": "INR",
                "notes": notes,
                "on_hold": True,
                "on_hold_until": 1671222870
                }
            ]
        }
        ans = db.find_one({"accountId": notes['teacher_account_id']})
        sheets = ans['sheets']
        sheets[notes['sheets']][int(notes['index'])]['status'] = "paid"
        db.update_one({"accountId": notes['teacher_account_id']}, {'$set': {'sheets': sheets}})
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Basic cnpwX3Rlc3RfMDZLTnN3UnFCZXlWQnM6MW9oQkNjRGJpSXdpdjlvV1RBWUpsVW5M'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return 'Receive'

# Main function
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=True)
