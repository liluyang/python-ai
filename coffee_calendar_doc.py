import calendar
import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set the month for the table
month = datetime.datetime.now().month
year = datetime.datetime.now().year

# Set up the Google Docs API client
credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/documents'])
service = build('docs', 'v1', credentials=credentials)
    
# Insert the table into the document
document_id = '1F13p5uxrfJnTDzITZGfBU5oBLGglMk5v8HGWYr2Ee20'

document = service.documents().get(documentId=document_id).execute()
index = document['body']['content'][3]['endIndex']
rowInx = 0

num_days = calendar.monthrange(year, month)[1]
num_rows = (num_days - 1) // 7 + 1
start_day = datetime.date(year, month, 1).weekday() + 1 

for row in range(num_rows):
    request1 = [{
        'insertTableRow': {
            'tableCellLocation': {
                'tableStartLocation': {'index': 2},
                'rowIndex': rowInx,
                'columnIndex': 1
            },
            'insertBelow': 'true'
        }
    }]
    service.documents().batchUpdate(documentId=document_id, body={'requests': request1}).execute()
    rowInx += 1
    
    for col in range(7):
        day = row * 7 + col + 1 - start_day + 1
        date_str = ' '
        if 1 <= day <= num_days:
            date_str = str(month) + '/' + str(day) + '\n'
        
        request2 = [{
            'insertText': {
                'location': {
                    'index': index
                },
                'text': date_str
            }
        }]
        index += len(date_str) + 2
        service.documents().batchUpdate(documentId=document_id, body={'requests': request2}).execute()
    index += 1 # next row 

