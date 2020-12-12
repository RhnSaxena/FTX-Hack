import requests
import json

def create_link(student,amount,teacher_account_id, index, filename):

    print(student)
    print(amount)

    print("rishi")

    url = "https://api.razorpay.com/v1/payment_links"

    print("rishi")

    payload= {
        "amount": amount*100,
        "currency": "INR",
        "accept_partial": True,
        "first_min_partial_amount": 100,
        "expire_by": 1691097057,
        "description": teacher_account_id,
        "notes": {
            'teacher_account_id':teacher_account_id,
            'index': index,
            'sheets': filename
            },
        "customer": student,
        "notify": {
            "sms": True,
            "email": True
        },
        "reminder_enable": True,
    }

    headers = {
    'Content-type': 'application/json',
    'Authorization': 'Basic cnpwX3Rlc3RfMDZLTnN3UnFCZXlWQnM6MW9oQkNjRGJpSXdpdjlvV1RBWUpsVW5M'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response.text