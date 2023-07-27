import json
from django.shortcuts import render,redirect
from bson import ObjectId
from pymongo import MongoClient
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd


# data=pd.read_csv("finalusers")
# data2=pd.read_csv("values")
# activeusers=data2["0"]
# str_values = [str(value) for value in activeusers]
# str_values
# filtered_df1 = data[data['user_id'].isin(str_values)]
# filtered_df1=filtered_df1[filtered_df1["client"].notnull()]
# # filtered_df1["client"].unique()
# clients=list(filtered_df1["client"].unique())
# clients
# filtered_df1[filtered_df1["client"]=="Reliable Kota"].shape[0]
# count={}
# for client in clients:
#     count[client]=filtered_df1[filtered_df1["client"]==client].shape[0]


# def setvariables(request):
#             client = request.POST.get('client_name')
#             date = request.POST.get('date')
#             print(client)
#             if client is not None and date is not None:
#                 print("hii")


#                 request.session['client'] = client
#                 request.session['date'] = date


#                 print(request.session.get('client'))
#                 print(request.session.get('date'))

#                 data=pd.read_csv("finalusers")
#                 data2=pd.read_csv("values")
#                 activeusers=data2["0"]
#                 filtered_df1 = data[data['user_id'].isin(activeusers)]
#                 filtered_df1=filtered_df1[filtered_df1["client"].notnull()]


#                 request.session['users'] =list(filtered_df1[filtered_df1["client"]==request.session['client']]["user_id"])

#                 client = MongoClient("mongodb://65.2.116.84:27017/")  # Replace with your MongoDB connection string
#                 db = client["production"]
#                 collection2 = db["users"]
#                 projection = {"_id": 1, "email": 1}

#                 usersobj = [ObjectId(value) for value in request.session['users']]

#                 users2 = collection2.find({"_id": {"$in": usersobj}}, projection)
#                 email_mapping = {str(user["_id"]): user["email"] for user in users2}


#                 request.session['email-mapping']=email_mapping
#                 print(request.session['email-mapping'])
#                 # request.session['users'] = [ObjectId(value) for value in request.session['users']]
#                 # print(request.session['users'])
#                 current_path = request.path
#             # Append "/session" to the current URL path
#                 new_path = current_path + 'client_session/'

#         # Redirect to the new URL
#                 return redirect(new_path)
#             # return render(request,'D:/data analysis/dataanalysis/myapp/templates/mainpage.html') 
#             count1=json.dumps(count)
#             context={
#                    'clients':count1
#             } 
#             return render(request,'client.html',context)

# def dataanalysis(request):
#     return render(request,'myapp/templates/mainpage')

# def set(request):

def setvariables(request):

    if request.method == 'POST':

        client = MongoClient("mongodb://65.2.116.84:27017/")  
        db = client["production"]  

        client = request.POST.get('client_name')
        startdate = request.POST.get('date')
        enddate = request.POST.get('edate')

        collection = db["clients"] 

        request.session['client']=client
        request.session['date'] = startdate
        request.session['edate'] = enddate

        phases = collection.find_one({"name": client})
        phase_ids = [str(phase) for phase in phases["phases"]]
        collection1=db['users']
        collection1.create_index("subscriptions.subgroups.phases.phase")

        pipeline = [
            {
                "$match": {
                    "subscriptions.subgroups.phases.phase": {"$in": [ObjectId(phase_id) for phase_id in phase_ids]}
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "email": 1
                }
            }
        ]

        result = collection1.aggregate(pipeline)

        user_dict = {str(user["_id"]): user["email"] for user in result}

        request.session['email-mapping']=user_dict

        request.session['users']=list(user_dict.keys())
        # print(len(request.session['users']))
        # request.session["obj_user"]=[ObjectId(user)  for user in request.session['users']]

        current_path = request.path
        new_path = current_path + 'activeuser/'



        def get_phase_data():
            pipeline = [
                {
                    '$unwind': '$phases'
                },
                {
                    '$lookup': {
                        'from': 'phases',
                        'localField': 'phases',
                        'foreignField': '_id',
                        'as': 'phase_info'
                    }
                },
                {
                    '$project': {
                        '_id': 0,
                        'client': '$name',
                        'phase_id': '$phases',
                        'phase_name': { '$arrayElemAt': [ '$phase_info.name', 0 ] }
                    }
                },
                {
                    '$group': {
                        '_id': '$client',
                        'phases': {
                            '$push': {
                                'phase_id': '$phase_id',
                                'phase_name': { '$ifNull': ['$phase_name', 'Phase Not Found'] }
                            }
                        }
                    }
                }
            ]

            result = db['clients'].aggregate(pipeline)

            data = []
            for item in result:
                client = item['_id']
                phases = item['phases']
                for phase in phases:
                    data.append({
                        'client': client,
                        'phase_id': phase['phase_id'],
                        'phase_name': phase['phase_name']
                    })

            return pd.DataFrame(data)

        df = get_phase_data()


        filterByClient=df[df["client"]==request.session["client"]]

        phases=filterByClient["phase_name"]
        
        totalPhasesOfClient=len(phases)

        request.session["totalPhasesOfclient"]=totalPhasesOfClient
        request.session["clientDataframe"]=filterByClient.to_json(orient='records',force_ascii=False, date_format='iso', default_handler=str)
            

        return redirect(new_path)
    return render(request,'client.html')
