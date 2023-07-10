import json
from django.shortcuts import render
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId


def get_total_logins(emails, api, start_date, end_date):
    # Connect to the MongoDB server
    client = MongoClient('mongodb://65.2.116.84:27017/')
    db = client.production
    collection = db.logs

    login_counts = {}

    current_date = start_date
    while current_date < end_date:
        query = {
            'params.email': {'$in': emails},
            'api': api,
            'createdAt': {'$gte': current_date, '$lt': current_date + timedelta(days=1)}
        }

        total_logins = collection.count_documents(query)

        login_counts[current_date.date()] = total_logins

        current_date += timedelta(days=1)

    client.close()

    return login_counts

def usage_graph(request):
    # if request.method == 'POST':
        # client_name = request.POST['client_name']
        client_name= request.session['client']
        csv_file_path = r"D:\data analysis\dataanalysis\finalusers"
        df=pd.read_csv(csv_file_path,low_memory=False)
        filtered_df = df[df['client'] == client_name]
        user_ids = filtered_df['user_id'].tolist()

        client = MongoClient("mongodb://65.2.116.84:27017/")  
        db = client["production"]
        collection = db["users"]
        def get_emails_by_user_ids(user_ids):
            object_ids = [ObjectId(user_id) for user_id in user_ids]

            query = {"_id": {"$in": object_ids}}
            projection = {"email": 1}  # Only retrieve the "email" field
            documents = collection.find(query, projection)
            emails = [doc["email"] for doc in documents if "email" in doc]

            return emails

        emails = get_emails_by_user_ids(user_ids)
        # start_date = datetime.strptime(request.POST['start_date'], "%Y-%m-%d")
        start_date = datetime.strptime(request.session['date'], "%Y-%m-%d")

        end_date = start_date + timedelta(days=7)

        # Retrieve the emails for the given client_name
        # Replace with your code to get the emails based on client_name

        # Calculate login counts
        login_counts = get_total_logins(emails, "users /signin", start_date, end_date)

        # Prepare data for the graph
        graph_data = []
        for date, count in login_counts.items():
            graph_data.append({'date': date, 'count': count})
        
        # graph_data = [
        # {'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in graph_data]
        # print(graph_data)
        # graph_data = json.dumps(graph_data)
        # # Pass the graph data to the template
        # context = {'graph_data': graph_data}
        # return render(request, 'client_usage_graph.html', context)
    
        graph_data_serializable = [
        {'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in graph_data
    ]

        graph_data_json = json.dumps(graph_data_serializable)
        print(graph_data_json)
        context = {'graph_data_json': graph_data_json}
        return render(request, 'client_usage_graph.html', context)

    # return render(request, 'client_usage_form.html')

