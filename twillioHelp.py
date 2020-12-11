from twilio.rest import Client
from urlpath import URL
import requests
import time
import csv
import personal_config
import config

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

if __name__ == "__main__":
    url = "https://api.twilio.com/2010-04-01/Accounts/ACee88cc6b6cf96910936801fa3726ccb5/Messages/MM2fb4f534d37e75bc93ec1daad6699373/Media/MEe5fe52624fc4d3e98e8439a14fb1625d";
    DownloadFile(url,"unique","files/")
    to_="whatsapp:+14155238886"
    from_="whatsapp:+918604074906"
    client = Client(account, token)
    print(sendSMS(client, to_, from_, "Siddharth"))
