import calendar
import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set the month for the table
month = 6
month_name = calendar.month_abbr[month]
year = datetime.datetime.now().year

# Set up the Google Docs API client
credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/spreadsheets'])
service = build('sheets', 'v4', credentials=credentials)
    
# Insert the table into the document
# document_id = '1F13p5uxrfJnTDzITZGfBU5oBLGglMk5v8HGWYr2Ee20' (google document)
spreadsheet_id = '1LkY4bBjeqJ51bCjs6CQcuBF4nG9Cj_OSOgA7e0etMyk' # google spreadsheet

# Retrieve the existing sheet data
sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
sheet_title = sheet['sheets'][0]['properties']['title']
sheet_range = f'{sheet_title}'  # Adjust the range as needed

# Create the date values
num_days = calendar.monthrange(year, month)[1]
num_rows = (num_days - 1) // 7 + 1
start_day = datetime.date(year, month, 1).weekday() + 1 

values = []
for row in range(num_rows):
    dates = []
    for col in range(7):
        day = row * 7 + col + 1 - start_day + 1
        if 1 <= day <= num_days:
            date = datetime.datetime(year, month, day, tzinfo=pytz.UTC)
            date_str = str(month) + '/' + str(day) + '\n '
            dates.append(date_str)
        else:
            dates.append('')
    values.append(dates)

# Prepare the update request
body = {
    'values': values
}
request = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=sheet_range,
    valueInputOption='RAW',
    body=body
)

# Execute the update request
response = request.execute()
