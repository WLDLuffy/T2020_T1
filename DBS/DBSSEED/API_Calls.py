import json
import requests

team_headers = {'identity': 'T79', 'token': 'b59c435b-eb62-4348-ab70-78b331848d04'}
username = "limzeyang"


def monthlyExp(accountId):
    months = [11]
    for month in months:
        url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/{accountId}?from={month}-01-2019&to={month}-30-2019"
        response = requests.get(url, headers=team_headers)

        if response.status_code == 200:
            data = response.json()
            length = len(data)
            x = 0
            totalAmt = 0
            while x < length:
                #print(data[x]['amount'])
                totalAmt += float(data[x]['amount'])
                x+=1
            print("Total Expenditure", round(totalAmt, 2))
        else:
            print("monthlyExp Error")
#for x in username:

def monthlyBal(accountId):
    months = [11]
    for month in months:
        url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/{accountId}/balance?month={month}&year=2019"
        response = requests.get(url, headers=team_headers)
        if response.status_code == 200:
            data = response.json()
            print("Monthly Balance",month,": ", data["availableBalance"])
        else:
            print("monthlyBal Error")

def ListofDepAcc(customerId):
    url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/{customerId}"
    response = requests.get(url, headers=team_headers)

    if response.status_code == 200:
        data = response.json()
        length = len(data)
        x = 0
        while x < length:
            print("accountId: ", data[x]['accountId'])
            monthlyBal(data[x]['accountId'])
            monthlyExp(data[x]['accountId'])
            x += 1
    else:
        print("ListofDepAcc Error")

def CustDet(customerId):
    url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/{customerId}/details"
    response = requests.get(url, headers=team_headers)
    if response.status_code == 200:
        data = response.json()["riskLevel"]
        print("riskLevel: ", data)


url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/{username}"
response = requests.get(url, headers=team_headers)
if response.status_code == 200:
    print("username: ", username)
    data = response.json()["customerId"]
    print("customerId: ", data)
    CustDet(data)
    ListofDepAcc(data)

