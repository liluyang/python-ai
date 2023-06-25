import calendar
import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set the month for the table
month = 7
month_name = calendar.month_abbr[month]
year = datetime.datetime.now().year

# Set up the Google Docs API client
credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/documents'])
service = build('docs', 'v1', credentials=credentials)

# Create a new table
dates = []
for day in range(1, 32):
    try:
        date = datetime.datetime(year, month, day, tzinfo=pytz.UTC)
        dates.append([date.strftime('%m/%d')] + [''] * 6)
    except ValueError:
        # Skip days that don't exist in the current month
        pass
    
# Insert the table into the document
document_id = '1F13p5uxrfJnTDzITZGfBU5oBLGglMk5v8HGWYr2Ee20'
rows = [
    [
        {
            'text': '1'
        },
        {
            'text': '2'
        }
    ],
    [
        {
            'text': '3'
        }
    ]
]
columns = [
    {
        'text': '1'
    },
    {
        'text': '2'
    }
]

requests = [
    {
        'insertTable': {
            'rows': rows, #round(len(dates)/7),
            'columns': columns,
            'endOfSegmentLocation': {
                'segmentId': ''
                # 'index': 0
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 1
            },
            'text': f'{month_name}\n'
        }
    }
]

service.documents().batchUpdate(
    documentId=document_id, 
    body={
        'requests': requests
    }
).execute()


requests = [
    {
        'insertText': {
            'location': {
                'index': 6
            },
            'text': '06/01'
        }
    }
]

# days_in_month = calendar.monthrange(year, month)[1]
# first_day = calendar.weekday(year, month, 1)
#
# for day in range(1, days_in_month + 1):
#     day_of_week = (day - 1 + first_day) % 7
#     table['rows'].append({
#         'cells': [
#             {
#                 'text': '{:02d}'.format(day)
#             }
#         ] * day_of_week
#     })
#
# requests = [{
#     'insertTable': {
#         'table': table
#     }
# }]

service.documents().batchUpdate(
    documentId=document_id, 
    body={
        'requests': requests
    }
).execute()

# print(f'Table for month {month} inserted into document "{document_id}"')
