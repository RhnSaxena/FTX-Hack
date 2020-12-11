from twilio.rest import Client
from flask import Flask, request
import personal_config
import twillioHelp as tw
import config

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
    from_number = request.form['From']
    to_number = request.form['To']
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
    print(request.get_json())
    return 'Receive'

# Main function
if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=True, threaded=True)
