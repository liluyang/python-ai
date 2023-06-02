import datetime
import pytz
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Set the month for the table
month = 4  # April

# Set up the Google Docs API client
creds = Credentials.from_authorized_user_file('credentials.json', ['https://www.googleapis.com/auth/documents'])
service = build('docs', 'v1', credentials=creds)

# Create a new table
table_rows = []
for day in range(1, 32):
    try:
        date = datetime.datetime(2023, month, day, tzinfo=pytz.UTC)
        table_rows.append([date.strftime('%m/%d')] + [''] * 6)
    except ValueError:
        # Skip days that don't exist in the current month
        pass
    
# Insert the table into the document
document_id = 'DOCUMENT_ID_HERE'
requests = [
    {
        'createTable': {
            'rowCount': len(table_rows),
            'columnCount': 7,
            'location': {
                'index': 0
            }
        }
    },
    {
        'insertText': {
            'location': {
                'index': 0
            },
            'text': f'Monthly Table {month}\n'
        }
    },
    {
       'insertTableRows': {
            'tableStartLocation': {
                'index': 0
            },
            'insertBelow': False,
            'number': len(table_rows)
        }
    },
    {
        'insertTableRow': {
            'tableCellLocation': {
                'tableStartLocation': {
                    'index': 0
                },
                'rowIndex': 0,
                'columnIndex': 0
            },
            'insertBelow': False,
            'cells': [{'text': cell} for cell in ['Day'] + [''] * 6]
        }
    },
    {
        'insertText': {
            'location': {
                'index': 0
            },
            'text': '\n'
        }
    },
    {
        'insertText': {
            'location': {
                'index': 0
            },
            'text': '\n'.join(['\t'.join(row) for row in table_rows])
        }
    }
]
service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()

print(f'Table for month {month} inserted into document "{document_id}"')
