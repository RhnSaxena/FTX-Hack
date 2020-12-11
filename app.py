from twilio.rest import Client
from flask import Flask, request
import twillioHelp as tw
import personal_config
import requests
import config
import json

# App initialize
app = Flask(__name__)


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
    if NumMedia != '0':
        Media = request.form['MediaUrl0']
    if body[0] == "/":
        print("It is a command.")
        tw.sendSMS(client, to_, from_, "It is command")
    else:
        print("It is a generic message.")
        tw.sendSMS(client, to_, from_, "It is Generic Message")
    return 'Receive'

@app.route('/callback', methods=['POST', 'GET'])
def callback():
    print(request.method)
    captureObject = request.get_json()
    print(captureObject["event"])
    if captureObject["event"] == "payment_link.paid":

        accountId="acc_GBihjkqRxFr1f6"
        url = "https://api.razorpay.com/v1/payments/{}/transfers/".format(captureObject["payload"]["payment"]["entity"]["id"])
        
        payload=  {
            "transfers": [
                {
                "account":accountId,
                "amount": captureObject["payload"]["payment"]["entity"]["amount"],
                "currency": "INR",
                "notes": {
                    "name": "Gaurav Kumar",
                    "roll_no": "IEC2011025"
                },
                "on_hold": True,
                "on_hold_until": 1671222870
                }
            ]
        }

        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Basic cnpwX3Rlc3RfMDZLTnN3UnFCZXlWQnM6MW9oQkNjRGJpSXdpdjlvV1RBWUpsVW5M'
        }

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return 'Receive'

# Main function
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=True)
