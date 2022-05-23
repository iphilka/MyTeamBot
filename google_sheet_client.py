import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Авторизуемся
CREDENTIALS_FILE = 'kodlandteamleads-a6f0cecf7bf5.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
