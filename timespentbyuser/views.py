from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import matplotlib
matplotlib.use('Agg')

def get_session_time(user_id, date):
    # Replace with your MongoDB connection string
    client = MongoClient("mongodb://65.2.116.84:27017/")
    db = client["production"]
    collection = db["sessions"]

    start_date = datetime(date.year, date.month, date.day)
    end_date = start_date + timedelta(days=1)

    sessions = collection.find({"user": ObjectId(user_id), "createdAt": {"$gte": start_date, "$lt": end_date}})
    total_time_spent = timedelta()

    for session in sessions:
        if "endTime" not in session:
            continue

        start_time = session["startTime"]
        end_time = session["endTime"]
        time_spent = end_time - start_time
        total_time_spent += time_spent

    if total_time_spent.total_seconds() == 0:
        return timedelta()  # Return timedelta object instead of a string

    return total_time_spent

def session_activity(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()

        labels = []
        values = []

        for i in range(7):
            current_date = start_date + timedelta(days=i)
            result = get_session_time(user_id, current_date)
            labels.append(current_date.strftime('%Y-%m-%d'))
            values.append(result.total_seconds() / 3600)  # Convert to hours

        # Create a bar graph
        print(values)
        print(labels)

        plt.bar(labels, values)
        plt.ylabel('Time Spent (Hours)')
        plt.title('Time Spent for Next 7 Days')
        plt.xticks(rotation=90)

        # Save the graph to a file
        graph_filename = 'graph.png'
        plt.switch_backend('agg')

        plt.savefig('timespentbyuser/static/' + graph_filename)
        plt.close()
        context = {
                    'user_id': user_id,
                    'date': start_date,
                    'graph_image': graph_filename,
                }
        # Render the HTML template with the graph image path
        return render(request, 'graph.html',context)

    return render(request, 'form.html')


