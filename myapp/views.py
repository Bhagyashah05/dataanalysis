from django.http import HttpResponse
import json
from django.shortcuts import render
import pandas as pd
from pymongo import MongoClient
import re
import os
from datetime import datetime
from bson import ObjectId


client = MongoClient("mongodb://65.2.116.84:27017/")  

db = client["production"]  

# collection = db["users"] 

# data = collection.find({}, {"_id": 1, "settings.goal": 1})

# data_list = []

# for document in data:
#     user_id = document.get("_id")
#     goals = document.get("settings", {}).get("goal")
#     data_list.append({"user_id": user_id, "goal": goals})

# df = pd.DataFrame(data_list)


# pattern = r"(\w{3} \w{3} \d{2} \d{4} \d{2}:\d{2}:\d{2})"


# df["goal"] = df["goal"].apply(lambda x: [
#     pd.to_datetime(re.search(pattern, entry["date"]).group()) for entry in x if entry is not None
# ] if isinstance(x, list) else [])

# filtered_df = df[df["goal"].apply(lambda x: any(date >= pd.to_datetime("2022-12-31") for date in x))]
# user_id=filtered_df['user_id']
# values=list(user_id)
# values=pd.read_csv(r"D:\data analysis\dataanalysis\values")
# values=list(values["0"])

# csv_file_path = r"D:\data analysis\dataanalysis\finalusers"
# users1=pd.read_csv(csv_file_path,low_memory=False)
# str_values = [str(value) for value in values]

# filtered_df1 = users1[users1['user_id'].isin(str_values)]
# # filtered_df3 = filtered_df1[(filtered_df1['client'] == 'Reliable Kota') | (filtered_df1['client'] == 'Reliable Kota')]
# filtered_df3=""



# users/views.py
def rel_form(request):
        # if request.method == 'POST':
        #     rel_value = request.session.get('client')
        #     filtered_df3 = filtered_df1[(filtered_df1['client'] == rel_value) ]
        #     rel=len(filtered_df3)
        #     return render(request, 'rel_value.html', {'rel': rel,'rel_value':rel_value})
        # else:
        #     return render(request, 'rel_value.html')


        start_date = request.session['date']
        start_date=datetime.strptime(start_date, "%Y-%m-%d")
         # Replace with your desired start date
        end_date = request.session['edate']  # Replace with your desired end date
        end_date=datetime.strptime(end_date, "%Y-%m-%d")
        obj_user=[ObjectId(user)  for user in request.session['users']]
        print(len(request.session["users"]))
        print(len(obj_user))
        attendance_query = {
                        'createdAt': {'$gte': start_date, '$lte': end_date}
                        }
        attendancepipeline = [
                        {"$match": attendance_query},
                        {"$unwind": "$users"},
                        {"$match": {"users.user": {"$in": obj_user}}},
                        {"$project": {"user_id": "$users.user"}}
                        ]
        attendances_result = db['attendances'].aggregate(attendancepipeline)                

        api="users /signin"
        logs_query = {
        "api": api,
        "createdAt":{
                "$gte": start_date,
                "$lte": end_date
        }
        }

        logs_results = db['logs'].find(logs_query)
 
        
        # Query the 'flowlogs' collection to find users with matching user IDs
        flowlogspipeline = [
        {
                "$match": {
                "user": {"$in": request.session["users"]},
                "createdAt": {
                        "$gte": start_date,
                        "$lte": end_date
                }
                }
        },
        {
                "$group": {
                "_id": "$user"
                }
        }
        ]

        flowlogs_results = db["flowlogs"].aggregate(flowlogspipeline)
        

        practice_logs = {
        "user": {"$in": request.session['users']},
        "createdAt":{
                "$gte": start_date,
                "$lte": end_date
        }
        }

        practice_logs_result = db["practicelogs"].find(practice_logs)
        # Query the 'attendance' collection to find users with matching user IDs

        # attendance_query = {
        #     "user_id": {"$in": user_ids}
        # }
        # attendance_results = attendance_collection.find(attendance_query)

        # Query the 'uservideostats' collection to find users with matching user IDs and updatedAt dates
        uservideostats_query = {
        "u": {"$in": obj_user},
        "updatedAt": {
                "$gte": start_date,
                "$lte": end_date
        }
        }

        uservideostats_results = db["uservideostats"].find(uservideostats_query)

        newusers={
                "_id": {"$in": obj_user},
                "createdAt":{
                "$gte": start_date,
                "$lte": end_date
                 }
        }

        usersCreatedCount=db['users'].count_documents(newusers)

        usersCreated=db['users'].find(newusers)

        videos={
               "createdBy":{"$in":obj_user},
                "createdAt":{
                "$gte": start_date,
                "$lte": end_date
                 }
        }

        videoslist=[]
        videosCreatedCount=db["videos"].count_documents(videos)

        clientjson= request.session.get('clientDataframe')
        clientdf=pd.read_json(clientjson,orient="records")
        phaseObjectIds=set(clientdf["phase_id"])
        phaseObjectIds= [ObjectId(phase) for phase in phaseObjectIds]
        # print(type(phaseObjectIds[0]))
        testpipeline = [
        {
            '$match': {
                'phases.phase': { '$in': phaseObjectIds },
                'createdAt': { '$gte': start_date, '$lte': end_date }
            }
        },
        {
            '$group': {
                '_id': '$type',
                'count': { '$sum': 1 }
            }
        }
    ]



        result = db['assessmentwrappers'].aggregate(testpipeline)

        test_counts = {item['_id']: item['count'] for item in result}
        print(test_counts)

        videosName=db["videos"].find(videos)

        for video in videosName:
                x=video["title"]
                videoslist.append(x)
        # videoslist=set(videoslist)
        videoslist=[[video] for video in videoslist]

        print("done")

        # print(videoslist)

        activeusers=[]

        for doc in usersCreated:
                x=doc['_id']
                activeusers.append(str(x))

        print("users created")
        print(len(set(activeusers)))

        for doc in attendances_result:
                                user_id = doc.get('user_id')
                                activeusers.append(str(user_id))
        print("attendance taken")
        print(len(set(activeusers)))

                
        for users in uservideostats_results:
                x=users['u']
                activeusers.append(str(x))
        print(len(set(activeusers)))

        
        
        activeusers.append(str(user['_id']) for user in flowlogs_results)
        
        
        for users in practice_logs_result:
                x=users['user']
                activeusers.append(x)
                
        print("practice done")
        print(len(set(activeusers)))

        


        

        userlogins=[]
        
        for users in logs_results:
                x=users["params"]["email"]
                userlogins.append(x)
        print(len(set(activeusers)))

        print("logs done")
        userdict=request.session['email-mapping']
        mails=userdict.values()
        mails=set(mails)
        userlogins=[email for email in userlogins if email in mails]
        totallogins=len(userlogins)
        uniquelogins=len(set(userlogins))

        usersUniqueLogins=list(set(userlogins))
        usersUniqueLogins=[[user] for user in usersUniqueLogins]

        print("users unique logins done")

        
        userlogins=set(userlogins)
        for key,value in userdict.items():
                if value in userlogins:
                        activeusers.append(str(key))
        
        userlist=set(activeusers)
        

        # print(userlist)
        # user_ids_objectids=[]
        # for id in userlist:
        #         user_ids_objectids.append(ObjectId(id))

        # print(user_ids_objectids)

#         objuserlist=list(ObjectId(user) for user in userlist)
#         

        filtered_user_dict = {key: value for key, value in userdict.items() if key in userlist}
        # print(filtered_user_dict)
        userlist=list(filtered_user_dict.values())
        rel=len(userlist)
        useridlist=list(filtered_user_dict.keys())
        useridobjectlist=[ObjectId(id) for id in useridlist]
        
        phaseuserspipeline = [
        {
                "$match": {
                "subscriptions.subgroups.phases.phase": {"$exists": True}
                }
        },
        {
                "$unwind": "$subscriptions"
        },
        {
                "$unwind": "$subscriptions.subgroups"
        },
        {
                "$unwind": "$subscriptions.subgroups.phases"
        },
        {
                "$group": {
                "_id": "$subscriptions.subgroups.phases.phase",
                "users": {"$addToSet": "$_id"}
                }
        },
        {
                "$match": {
                "users": {"$in": useridobjectlist}
                }
        },
        {
                "$project": {
                "phase_id": "$_id",
                "user_count": {"$size": "$users"}
                }
        }
        ]

        phaseusersresult = db['users'].aggregate(phaseuserspipeline)
        phase_user_count_dict = {}

# Search for phase names in the "phases" collection and update the dictionary
        for doc in phaseusersresult:
                phase_id = str(doc['phase_id'])
                phase_doc = db['phases'].find_one({"_id": ObjectId(phase_id)})
                if phase_doc:
                        phase_name = phase_doc.get('name')
                        phase_user_count_dict[phase_name] = doc['user_count']
        phase_user_count = [{'name': key, 'y': value} for key, value in phase_user_count_dict.items()]
        phase_user_count=json.dumps(phase_user_count)

        phase_user_count_tableformat=[[key,value] for key ,value in phase_user_count_dict.items()]
        phase_user_count_tableformat=json.dumps(phase_user_count_tableformat)
        twodusers=[[user] for user in userlist]

        twodusers=json.dumps(twodusers) 
        usersUniqueLogins=json.dumps(usersUniqueLogins)
        videoslist=json.dumps(videoslist)
        tuser=len(request.session['users'])
        return render(request,"rel_value.html",{'rel':rel,'tuser':tuser,'userlist':twodusers,'usersCreatedCount':usersCreatedCount,'totallogins':totallogins,'uniquelogins':uniquelogins,'usersUniqueLogin':usersUniqueLogins,'videosCreatedCount':videosCreatedCount,'videolist':videoslist,'totalPhases':request.session['totalPhasesOfclient'],'testCount':test_counts,"phaseUserCount":phase_user_count,'phase_user_count_tableformat':phase_user_count_tableformat})






def mainpage(request):
        return render(request,'mainpage.html')   




def phases(request):
      
                return HttpResponse("Under Construction")

                





