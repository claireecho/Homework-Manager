from __future__ import print_function

import os.path

from flask import Flask, request, render_template, redirect

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

app.static_folder = 'static'

@app.route('/')
def index():
    data = main()['items']
    data = sortByDate(data)
    return render_template('index.html', data=data, convertDate=convertDate)

def convertDate(date):
    #YYYY-MM-DD
    MONTH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', "Jun", 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    day = int(date[8:10])
    return f'{MONTH[int(date[5:7])-1]} {day}, {date[0:4]}'

def sortByDate(data):
    length = len(data)
    for x in range(0, length):
        if 'due' in data[x]:
            print(data[x])
            idX = int(data[x]['due'][0:4] + data[x]['due'][5:7] + data[x]['due'][8:10])
            for y in range(x+1, length):
                if 'due' in data[y]:
                    idY = int(data[y]['due'][0:4] + data[y]['due'][5:7] + data[y]['due'][8:10])
                    if idX > idY:
                        temp = data[x]
                        data[x] = data[y]
                        data[y] = temp
        else:
            data.append(data[x])
            data.pop(x)
            length -= 1
    return data

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']

LIST_NAME = "Homework Manager"


def main():
    '''Authenicate Google Users'''
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    redirect('/')

    try:
        service = build('tasks', 'v1', credentials=creds)
        
        results = service.tasklists().list().execute()

        id = findHWList(service)
        
        tasksList = service.tasks().list(tasklist=id, showCompleted=False).execute()
        return tasksList
            

        classes = ['CS 110', 'CS 211', 'HNRS 110', 'HNRS 122', 'HNRS 111', 'MATH 125']


        option = input('Selected Option: ')
        while option != 'e':
            print()
            if option == 'a':
                classIndex = input('Select a class:\n\n\t0: CS 110\n\t1: CS 211\n\t2: HNRS 110\n\t3: HNRS 122\n\t4: HNRS 111\n\t5: MATH 125\n\nSelected class: ')
                title = input('Assignment Name: ')
                dueDate = input('Due Date (Format: YYYY-MM-DD): ')
                print(f'{dueDate}T00:00:00.000Z')
                task = service.tasks().insert(tasklist=id, body={'title': f'{classes[int(classIndex)]}: {title}', 'due': f'{dueDate}T00:00:00.000Z'}).execute()
                print('\nSucessfully added new task\n')
            elif option == 'b':
                print("Here's the tasks you need to complete:\n")
                tasksList = service.tasks().list(tasklist=id, showCompleted=False).execute()
                for task in reversed(tasksList['items']):
                    print(f'\t{task["title"]}')
                    print(f'\tDue: {task["due"][0:10]}\n')
                print("\nPress [ENTER] when finished")
                input()
            option = input("Select one of the following options\n\n\ta: Create new task\n\tb: View all tasks\n\tc: Delete a task\n\td: Complete a task\n\te: Exit\n\nSelected Option: ")






    except HttpError as err:
        print(err)

# Finds the HW tasklist
def findHWList(service):
    
    results = service.tasklists().list().execute()

    LENGTH = len(results['items'])

    for data in results['items']:
        if LIST_NAME in data['title']:
            return data['id']
        
    new = service.tasklists().insert(body={
        "title": LIST_NAME
    }).execute()

    # prints to console that a new list was made
    print(f"!! CREATED A NEW LIST: \"{new['title']}\" !!\n")
    return new['id']



if __name__ == '__main__':
    main()