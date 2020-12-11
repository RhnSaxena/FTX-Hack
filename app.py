from flask_pymongo import PyMongo
from twilio.rest import Client
from flask import Flask, request
import personal_config
import twillioHelp as tw
import config

# App initialize
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://root:root@cluster0.g2z5c.mongodb.net/test"
mongo = PyMongo(app)

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
    
    else:
        try:
            if body[0] == "/":
                command = body.split(" ")
                ctype = command[0]
                if len(command) > 1:
                    anytext = command[1]
                    if ctype.lower() == "/greet":
                        tw.sendSMS(client, to_, from_, "HI "+ anytext)
                else:
                    if ctype.lower()  == "/game":
                        tw.sendSMS(client, to_, from_, "i will play with you")
            else:
                print("I did not understand")
        except:
            tw.sendSMS(client, to_, from_, "I did not understand")
    return 'Receive'

@app.route('/callback', methods=['POST', 'GET'])
def callback():
    print(request.method)
    print(request.get_json())
    return 'Receive'

# Main function
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=True)
