# app/views.py
import json
from django.shortcuts import render
import datetime
import pytz
import matplotlib.pyplot as plt
from pymongo import MongoClient
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
from datetime import timedelta
from django.http import HttpResponse
from django.http import JsonResponse

# def get_user_login_times(email, api, start_date, end_date):
#         client = MongoClient('mongodb://65.2.116.84:27017/')

#         db = client.production
#         collection = db.logs

#         login_counts = {}

#         current_date = start_date
#         while current_date < end_date:
#             query = {
#                 'params.email': email,
#                 'api': api,
#                 'createdAt': {'$gte': current_date, '$lt': current_date + timedelta(days=1)}
#             }

#             total_logins = collection.count_documents(query)

#             login_counts[current_date.date()] = total_logins

#             current_date += timedelta(days=1)

#         client.close()

#         return login_counts , start_date

#     # api_name = "users /signin"
#     # start_date = "2023-06-14"
#     # email = "ruchik4822@keystone.com"

    

    
    
# # for users login

# def login_activity(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         api_name = request.POST.get('api_name')
#         start_date = request.POST.get('start_date')

#         start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
#         end_date = start_date + datetime.timedelta(days=7)
#         login_counts = get_user_login_times(email, api_name, start_date, end_date)
#     # for date, count in login_counts.items():
#     #     print(f"Date: {date}, Login Count: {count}")


#         # if start_date:
#         #     start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').astimezone(pytz.utc)
#         # else:
#         #     start_date = None

#         # login_count, start_date = get_user_login_times(email, api_name, start_date)
#         print(login_counts)
#         login_counts,_=login_counts
#         dates = list(login_counts.keys())
#         counts = list(login_counts.values())

#         # Convert dates to datetime objects with fixed time (midnight)
#         dates = [datetime.datetime.combine(date, datetime.time.min) for date in dates]

#         plt.bar(dates, counts, align='center')
#         plt.xlabel('Date')
#         plt.ylabel('Number of Logins')
#         plt.title('Login Activity')
#         plt.xticks(rotation=90, ha='right')

#         buffer = BytesIO()
#         plt.switch_backend('agg')

#         plt.savefig(buffer, format='png')
#         plt.close()

#         buffer.seek(0)
#         graph_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

#         context = {
#             'email': email,
#             'api_name': api_name,
#             'start_date': start_date,
#             'graph_image': graph_image,
#         }

#         return render(request, 'login_activity.html', context)
#     else:
#         return render(request, 'login_activity.html')


def login_activity(request):
    emailmapping=request.session['email-mapping']
    users=list(emailmapping.keys())
    emails=list(emailmapping.values())
    date=request.session['date']
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    print(date)

    client = MongoClient('mongodb://65.2.116.84:27017/')

    db = client.production
    collection = db['logs']

    query={
        'params.email': {'$in':emails},
        'createdAt': {'$gte': date, '$lt': date + timedelta(days=1)}
    }

    logs=collection.find(query)
    dict={}
    for email in emails:
        dict[email]=0
    for log in logs:
        # print("hii")
        email=log["params"]["email"]
        dict[email]=dict[email]+1

    # print(dict)
    table_data=[]
    for email, count in dict.items():
        table_data.append([email,count])
    table_data=json.dumps(table_data) 
    # print(table_data)
    

    return render(request,'login_activity.html',{'data':table_data})


def userlogin(request):

    email=request.GET.get('x')
    date=request.session['date']
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    end_date = date + datetime.timedelta(days=7)

    responsedata="done"
    client = MongoClient('mongodb://65.2.116.84:27017/')

    db = client.production
    collection = db.logs

    login_counts={}

    # total_logins = collection.count_documents(query)

    while date < end_date:
        query={
        'params.email': email,
        'api': 'users /signin',
        'createdAt': {'$gte': date, '$lt': date + timedelta(days=1)}
    }
        
        total_logins = collection.count_documents(query)

        login_counts[date.date()] = total_logins

        date += timedelta(days=1)

        responsedata = {str(key): value for key, value in login_counts.items()}
        
    # print(responsedata)



    return JsonResponse(responsedata,safe=False)
    