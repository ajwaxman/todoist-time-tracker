import requests  
import todoist
import csv
from pprint import pprint
from datetime import datetime


## IMPORTANT ## 
# Add your Todoist API token here
# You can find your token from the Todoist Web app at "Setttings > Integrations > API Token"
token = "1234567890abcdefghijkl"
api = todoist.TodoistAPI(token)
api.sync()


class Task:
    instances = []
    def __init__(self, id, content, date_created, time_created, time, energy, labels):
        self.id = id
        self.content = content
        self.date_created = date_created
        self.time_created = time_created
        self.time = time
        self.energy = energy
        self.labels = labels
        self.__class__.instances.append(self)

    @classmethod
    def printInstances(cls):
        for instance in cls.instances:
            pprint(vars(instance))
    
    @classmethod
    def addRows(cls):
        rows = []
        for instance in cls.instances:
            row_array = [instance.id, instance.content, instance.time, instance.energy, instance.labels, instance.date_created, instance.time_created]
            rows.append(row_array)
        return rows

items = api.state['items']
labels = api.state['labels']

label_names = {}

for l in labels:
    label_names[l['id']] = l['name']

times = ('15','30','45','60','75','90','105','120')


inbox = []

for i in items:
    
    ## IMPORTANT ## 
    # Add the id for whatever project you want to export items from for time tracking purposes
    # You can find this by visiting the project via Todoist's web app. Their URL structure is https://todoist.com/app/project/{project_id}
    if i['project_id'] == 123456789: 
        date_time_object = datetime.strptime(i['date_added'], '%Y-%m-%dT%H:%M:%SZ')
        task_labels = []
        energy = ""
        time = ""
        for label in i['labels']:
            label_name = label_names[label]
            task_labels.append(label_name)
            if label_name in (times):
                time = label_name
            if label_name == "gain":
                energy = "gain"
            if label_name == "drain":
                energy = "drain"
        Task(i['id'], i['content'], date_time_object.strftime("%m/%d/%Y"), date_time_object.strftime("%H:%M:%S"), time, energy, task_labels)


# Task.printInstances()

    
# field names  
fields = ['ID', 'Content', 'Time', 'Energy', 'Labels', 'Date Created', 'Time Created (UTC)']  
    
# # data rows of csv file 
rows = Task.addRows()
    
# name of csv file  
filename = "todoist.csv"
    
# writing to csv file  
with open(filename, 'w') as csvfile:  
    # creating a csv writer object  
    csvwriter = csv.writer(csvfile)  
        
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(rows) 
