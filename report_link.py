import requests
import json

def report_link(db,user_id,sheet_name,flag):
    user_detail = db.find_one({"user": user_id})

    # print("------------------------------------------")
    # print(user_detail)
    # print("-----------&&&&&&&&&&-------------------------------")
    # print(ans["sheets"][sheet_name])
    student = user_detail["sheets"][sheet_name]

    ans = []

    for st in student:
        if(flag == st["status"]):
            ans.append(st)


    print(ans)
    return ans

