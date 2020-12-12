import requests
import json
from generateReport import creation

def report_link(db,user_id,sheet_name,flag):
    user_detail = db.find_one({"user": user_id})

    # print("------------------------------------------")
    # print(user_detail)
    # print("-----------&&&&&&&&&&-------------------------------")
    # print(ans["sheets"][sheet_name])
    student = user_detail["sheets"][sheet_name]

    
    
    ans = []

    count =1
    for st in student:
        if(flag == st["status"]):
            st["sNo"]=count
            ans.append(st)
            count=count+1


    data ={
        "title":flag.lower(),
        "items":ans
    }

    return creation.createReport(data, sheet_name)

