# app/views.py
from django.shortcuts import render
import datetime
import pytz
import matplotlib.pyplot as plt
from pymongo import MongoClient
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')


def get_user_login_times(email, api_name, start_date=None):
    # Connect to the MongoDB server and access the collection
    client = MongoClient("mongodb://65.2.116.84:27017/")
    db = client["production"]
    collection = db["logs"]

    # Define the query based on the email, API name, and start date
    query = {"params.email": email, "api": api_name}
    if start_date:
        query["createdAt"] = {"$gte": start_date}

    # Fetch the documents matching the query
    documents = collection.find(query)
    
    # Initialize variables for login counts and the start date
    login_count = {}
    latest_login_time = None

    # Iterate through each document
    for document in documents:
        # Retrieve the createdAt time from the document
        created_at = document["createdAt"]
        ist = pytz.timezone('Asia/Kolkata')
        created_at = created_at.astimezone(ist)

        date = created_at.date()
        if date in login_count:
            login_count[date] += 1
        else:
            login_count[date] = 1

    if start_date and start_date.date() not in login_count:
        next_date = start_date.date()
        while next_date not in login_count:
            next_date += datetime.timedelta(days=1)
        start_date = next_date

    return login_count, start_date

def login_activity(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        api_name = request.POST.get('api_name')
        start_date_str = request.POST.get('start_date')

        if start_date_str:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').astimezone(pytz.utc)
        else:
            start_date = None

        login_count, start_date = get_user_login_times(email, api_name, start_date)

        dates = list(login_count.keys())
        counts = list(login_count.values())

        # Convert dates to datetime objects with fixed time (midnight)
        dates = [datetime.datetime.combine(date, datetime.time.min) for date in dates]

        plt.bar(dates, counts, align='center')
        plt.xlabel('Date')
        plt.ylabel('Number of Logins')
        plt.title('Login Activity')
        plt.xticks(rotation=90, ha='right')

        buffer = BytesIO()
        plt.switch_backend('agg')

        plt.savefig(buffer, format='png')
        plt.close()

        buffer.seek(0)
        graph_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        context = {
            'email': email,
            'api_name': api_name,
            'start_date': start_date_str,
            'graph_image': graph_image,
        }

        return render(request, 'login_activity.html', context)
    else:
        return render(request, 'login_activity.html')
