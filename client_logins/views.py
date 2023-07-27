import json
from django.shortcuts import render
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId


def get_total_logins(emails, api, start_date, end_date):

    
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

        emails=request.session['email-mapping']
        emails=list(emails.values())
     
        print(emails)
        start_date = datetime.strptime(request.session['date'], "%Y-%m-%d")

        end_date = start_date + timedelta(days=7)

        
        login_counts = get_total_logins(emails, "users /signin", start_date, end_date)

        graph_data = []
        for date, count in login_counts.items():
            graph_data.append({'date': date, 'count': count})
        
       
    
        graph_data_serializable = [
        {'date': item['date'].strftime('%Y-%m-%d'), 'count': item['count']} for item in graph_data
    ]

        graph_data_json = json.dumps(graph_data_serializable)
        print(graph_data_json)
        context = {'graph_data_json': graph_data_json}
        return render(request, 'client_usage_graph.html', context)

    # return render(request, 'client_usage_form.html')

