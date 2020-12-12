import imaplib
import base64
import os
import email
import requests
import json
import pymongo
import twillioHelp as tw
import pandas
import personal_config
import smtplib
import ssl
from email.message import EmailMessage

def sendEmail(text, toUser,subjectText):
    usr =personal_config.emailAddress
     
    pswd = personal_config.emailPassword

    msg = EmailMessage()
    msg.set_content(text)
    msg["Subject"] = subjectText
    msg["From"] = personal_config.emailAddress
    msg["To"] = toUser

    context=ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(usr, pswd)
        smtp.send_message(msg)
        print('Email was sent successfully!')
    
    return "Email Sent"





def readEmail():
    emailData = []
    email_user = personal_config.emailAddress
    email_pass = personal_config.emailPassword
    mail = imaplib.IMAP4_SSL("imap.gmail.com",993)
    mail.login(email_user, email_pass)
    mail.select('Inbox')
    type, data = mail.search(None, 'UNSEEN', '(SUBJECT "Fee Collect% ")')
    mail_ids = data[0]
    id_list = mail_ids.split()
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        mailSubject = str(email_message).split("Subject: ", 1)[1].split("\n", 1)[0] 
        sender = str(email_message).split("From: ", 1)[1].split("<", 1)[1].split(">", 1)[0]
        
        for part in email_message.walk(): 
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            
            fileName = part.get_filename()
            print(mailSubject)
            print(fileName)
            emailData.append({
                "user": mailSubject.split(" ")[3],
                "fileName": fileName,
                "mailerId":sender
            })

            if bool(fileName):
                cwd = os.path.join(os.getcwd(),"files") 
                filePath = os.path.join(cwd, fileName)

                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    return emailData
    



if __name__ == "__main__":
    while True:
        data=readEmail()
        if len(data) !=0:
            clientdb = pymongo.MongoClient("mongodb+srv://root:root@cluster0.g2z5c.mongodb.net")
            # clientdb = pymongo.MongoClient("mongodb://localhost:27017")
            db = clientdb.ftx.user
            for item in data:
                sendEmail("Thanks for using FTX Hack. We have received your request and are working on it.",item["mailerId"],"Request Received")
                print("This is the item")
                print(item)
                fileNameList =item["fileName"].split(".")
                ext= fileNameList[len(fileNameList)-1]
                if ext=="xlsx":
                    body = pandas.read_excel("./files/{}".format(item["fileName"]))
                    body=body.to_csv(r'./files/{}'.format(item["fileName"]), index=False)                    
                teacherData = db.find_one({"user": item["user"]})
                tw.readCSV("files/",item["fileName"],teacherData['accountId'],item["fileName"], item["user"], db, teacherData['sheets'])
                print("created links")
                sendEmail("Payment Links created, the customers will soon receive the links.",item["mailerId"],"Request Serviced")


