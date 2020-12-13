# FTX-Hack

## Description

A smart Spreadsheet based solution, that can be shared with a chatbot or sent over through an email, to subsequently generate payment links for payment collection.

## Prerequisite

1. Download ngrok <https://ngrok.com/> 
2. Twillio Account  with WhatsApp sandbox configured <https://www.twilio.com>
3. MongoDB and MONGODB Compass or you can use cli as one wishes\
Link Compass: <https://www.mongodb.com/try/download/compass> 
Link DB: <https://www.mongodb.com/try/download/community>
4. Python3.6 and pip installed
5. RazorPay account

## Steps To Run The Repository

1. Clone the repository.
2. Create a directory named `files` inside `FTX-HACK` directory.
3. Create a `personal_config.py` inside `FTX-HACK` directory , add your API keys for TWILLIO <https://www.twilio.com/console> \
  as follows: \

  ```bash
 SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 AUTH_TOKEN = "94xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
 MONGO_URL = "mongodb://user:password@localhost:27017/test"
 aws_config={
  "aws_access_key_id":"AXXXXXXXXXXXXXXXXXXXX", 
  "aws_secret_access_key":"xfxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}

aws_bucket={
  "bucket_name":"xxxxxx"
}

emailAddress="xxxxxxx@gmail.com"
emailPassword="**********"
```

4. Create Virtualenv `virtualenv venv --python=python3.6`
5. Start virtual env 
For Ubuntu : `source source ../env/bin/activate`
For Windows: `./env/bin/activate`
6. Run `pip install -r requirements.txt`
7. Start the server `python ./app.py`
8.  `./ngrok http 3000`
9. Add ngrok url into twilio <https://www.twilio.com/console/sms/whatsapp/sandbox> in **when message comes in** field.
10. Add webhook event `payment_link.paid` through Razorpay Account to send callback to main server for payment settlement.

## Database Structure

````bash
{
    "user": "whatsapp:+919999999999",
    "accountId": "acc_xxxxxxxxxxxxxx",
    "sheets": {
        "file1": [{
            "name": "Rishi Agrawal",
            "contact": "+91888888888",
            "email": "rishi@gmail.com",
            "amount": 5,
            "TransactionId": "plink_xxxxxxxxxxxxxx",
            "status": "unpaid"
        }, {
            "name": "Siddharth",
            "contact": "+917777777777",
            "email": "siddharth@gmail.com",
            "amount": 10,
            "TransactionId": "plink_xxxxxxxxxxxxxx",
            "status": "unpaid"
        }],
    }
}
````

## Flow (use case) for Tution teacher for payments

![Flow](/images/mermaid.png)

## Software Features
1) User just have to upload file having his customer Name, Phone number, Email, Amount.
2) Just one command to share link to 1000s of customers. 
3) User payment settle after each payment. 
2) User can get instant report of paid/unpaid Transaction

## Screenshots
![you can share sheet with Whatsapp](/images/sharewithwhatsapp.png)
![you can share sheet with Google Docs](/images/sharewithdocs.png)
![you can share sheet with Email also](/images/sharewithemail.png)
![To get report](/images/togetreport.png)
![Example Report](/images/report.png)
