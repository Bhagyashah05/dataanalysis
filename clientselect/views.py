import json
from django.shortcuts import render,redirect


import pandas as pd


data=pd.read_csv("finalusers")
data2=pd.read_csv("values")
activeusers=data2["0"]
str_values = [str(value) for value in activeusers]
str_values
filtered_df1 = data[data['user_id'].isin(str_values)]
filtered_df1=filtered_df1[filtered_df1["client"].notnull()]
# filtered_df1["client"].unique()
clients=list(filtered_df1["client"].unique())
clients
filtered_df1[filtered_df1["client"]=="Reliable Kota"].shape[0]
count={}
for client in clients:
    count[client]=filtered_df1[filtered_df1["client"]==client].shape[0]


def setvariables(request):
            client = request.POST.get('client_name')
            date = request.POST.get('date')
            print(client)
        # Check if the client and date are not None before processing
            if client is not None and date is not None:
                print("hii")
            # Store the client and date in the session
                request.session['client'] = client
                request.session['date'] = date
                print(request.session.get('client'))
                print(request.session.get('date'))
                # return redirect('analysis_view')

                current_path = request.path
            # Append "/session" to the current URL path
                new_path = current_path + 'activeuser/'

        # Redirect to the new URL
                return redirect(new_path)
            # return render(request,'D:/data analysis/dataanalysis/myapp/templates/mainpage.html') 
            count1=json.dumps(count)
            context={
                   'clients':count1
            } 
            return render(request,'client.html',context)

# def dataanalysis(request):
#     return render(request,'myapp/templates/mainpage')

# def set(request):

      