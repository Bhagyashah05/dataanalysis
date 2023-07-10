import json
from django.shortcuts import render
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd
from bson import ObjectId
from django.http import HttpResponse
# Create your views here.


def get_session_time(user_ids,date):
        client = MongoClient("mongodb://65.2.116.84:27017/")
        db=client["production"]
        collection=db["sessions"]

        startdate=datetime(date.year,date.month,date.day)
        end_date=startdate+timedelta(days=1)

        query={
                "user": {"$in": user_ids},
                "createdAt":{"$gte":startdate,"$lt":end_date}
        }
        sessions=collection.find(query)

        total_time_spent=timedelta()
        
        if sessions is None:
                return str(timedelta(0))
        for session in sessions:

                if "endTime" not in session:
                        continue
                start_time=session["startTime"]
                end_time=session["endTime"]
                time_spent=end_time-start_time
                # print(time_spent)
                total_time_spent+=time_spent
        if total_time_spent.total_seconds()==0:
                return timedelta()
        else:
             total_time_spent=round(total_time_spent.total_seconds()/3600,2)
             
        # print(topics)
        return total_time_spent

def userids(request):
        # if request.method=='POST':
                print("run")
                client_name=request.session.get('client')
                start_date=datetime.strptime(request.session.get('date'),'%Y-%m-%d').date()
                # print(start_date)
                # print(client_name)
                # start_date='2023-06-17'
                # start_date=datetime.strptime(start_date,'%Y-%m-%d').date()
                # client_name="Keystone Universe of Education"
                csv_file_path = r"D:\data analysis\dataanalysis\finalusers"
                df=pd.read_csv(csv_file_path,low_memory=False)
                filtered_df = df[df['client'] == client_name]
                user_ids = filtered_df['user_id'].tolist()
                # user_ids=[ObjectId('647dc6202e6949463c613615'),ObjectId('628c8d58fcc29215d1bb675f')]
                # print(type(user_ids[0]))
                user_ids=[ObjectId(item) for item in user_ids]
                # user_ids=tuple(user_ids)
                # print(user_ids)
                # total_time=get_session_time(user_ids,start_date)
                end_date=start_date+timedelta(days=7)
                dates=[]
                values=[]

                for day in range ((end_date-start_date).days+1):
                        current_date = start_date + timedelta(days=day)
    # Calculate the time for the current day
                        dates.append(str(current_date))
                        current_day_time  = get_session_time(user_ids, current_date)
                        values.append(str(current_day_time))
    # Store the time in the dictionary with the date as the key
                        # time_dict[current_date] = current_day_time
                data=dict(zip(dates,values))
                print(data)
                json_data=json.dumps(data)
                # print(json_data)
                # print(dates)
                context={
                        'data':json_data,
                        'client':client_name,
                        'date':start_date
                }


                return render(request,'client_session_graph.html',context)
        # return render(request,'from.html')



        





