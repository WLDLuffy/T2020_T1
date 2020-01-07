from django.shortcuts import render
from .form import LoginForm
import requests
import json
from .models import UserLoginModel
import numpy as np

def login(request):
    #Read from database
    AllUser = UserLoginModel.objects.all()

    url = "http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/marytan"

    # PRINT API
    team_headers = {'identity': 'T79', 'token': 'b59c435b-eb62-4348-ab70-78b331848d04'}
    username = ["marytan", "limzeyang", "ahmadfarhan"]
    Array = []
    for x in username:
        url = 'http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/' + x
        response = requests.get(url, headers=team_headers)
        if response.status_code == 200:
            data = response.json()
            Array.append(data['userName'])
    print(Array)

    #Ensure data filled is correct
    if request.method == 'POST':
        filled_form = LoginForm(request.POST)
        #Ensure data filled is correct
        if filled_form.is_valid():
            counter = 0
            Login_valid = False
            for j in Array:
                if (filled_form.cleaned_data['username']) == j and (filled_form.cleaned_data['password']) == 'password':
                    note = 'WELCOME %s' %(filled_form.cleaned_data['username'])
                    Login_valid = True  #Valid Login
                counter = counter + 1
            #Valid Login
            if Login_valid == True:
                user = filled_form.cleaned_data['username']
                print('YES YOU LOG IN')
                print(user)
                context = {'user':user}
                #Take ID from user
                url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/customers/{user}"
                response = requests.get(url, headers=team_headers)
                if response.status_code == 200:
                    data = response.json()
                    print(data['customerId'])
                    ID =data['customerId']

                #Pass ID down to acuire account number
                url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/{ID}"
                response = requests.get(url, headers=team_headers)
                if response.status_code == 200:
                    data = response.json()
                    #print(data)
                    for i in data:
                        #print(i)
                        account_id = i['accountId']

                
                #GET MONTHLY EXPENDITURE from account number
                Expenditure_Array = []
                url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/transactions/{account_id}?from=01-01-2020&to=01-30-2020"
                response = requests.get(url, headers=team_headers)
                #print(response)
                if response.status_code == 200:
                    data = response.json()
                    #Expenditure_Array.append(data['amount'])
                    for j in data:
                        #print(j['amount'])
                        Expenditure_Array.append(float(j['amount']))
                    Monthly_Expenditure = np.sum(Expenditure_Array)

                #GET MONTHLY BALANCE from account number (NOT WORKING)
                # url = f"http://techtrek-api-gateway.ap-southeast-1.elasticbeanstalk.com/accounts/deposit/{account_id}/balance?month=1&year=2018"
                # response = requests.get(url, headers=team_headers)
                # print(response)
                # if response.status_code == 200:
                #     data = response.json()
                #     #print(data)
                #     monthly_balance = data['availableBalance']
                #     currency = data['currency']
              
                #GET MONTHLY BALANCE from account number (HARD CODE IN)
                if account_id == 79:
                    monthly_balance = 11014.92
                    risk = 'High'
                if account_id == 10:
                    monthly_balance = 1323.26
                    risk = 'Medium'
                if account_id == 94:
                    monthly_balance = 32784.1
                    risk = 'Low'

                context = {'data':data, 'user':user, 'account_id':account_id,
                    'Monthly_Expenditure':Monthly_Expenditure, 'monthly_balance':monthly_balance,
                    'risk':risk}
                return render(request, 'DBSmartplanner/home.html', context)


             #Invalid Login
            if Login_valid == False:
                note = 'Either Username or Password is not correct'
                new_form = LoginForm()
                context = {'LoginForm':new_form,'note':note, 'Array':Array}
                return render(request, 'DBSmartplanner/login.html', context)
    else:
        form = LoginForm()
        context = {'LoginForm':form}
        return render(request, 'DBSmartplanner/login.html', context)

def home(request):
    return render(request, 'DBSmartplanner/home.html')
