from django.shortcuts import render
import pandas as pd
from pymongo import MongoClient
import re
import os

# client = MongoClient("mongodb://65.2.116.84:27017/")  

# db = client["production"]  

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
values=pd.read_csv(r"D:\user django\values")
values=list(values["0"])
values
csv_file_path = r"D:\user django\finalusers"
users1=pd.read_csv(csv_file_path,low_memory=False)
str_values = [str(value) for value in values]

filtered_df1 = users1[users1['user_id'].isin(str_values)]
# filtered_df3 = filtered_df1[(filtered_df1['client'] == 'Reliable Kota') | (filtered_df1['client'] == 'Reliable Kota')]
filtered_df3=""



# users/views.py


def rel_form(request):
    if request.method == 'POST':
        rel_value = request.POST.get('rel')
        filtered_df3 = filtered_df1[(filtered_df1['client'] == rel_value) ]
        rel=len(filtered_df3)
        return render(request, 'rel_value.html', {'rel_val': rel,'rel_value':rel_value})
    else:
        return render(request, 'rel_value.html')

def rel_value(request):
    # Your code here to calculate the 'rel' value or use the existing value
    # rel = len(filtered_df3)  # Calculate or use the 'rel' value from your code

    return render(request, 'rel_value.html', {'Active users': rel})
    
def mainpage(request):
    return render(request,'mainpage.html')

