#Update TestTestTest
import gspread
from google.oauth2.service_account import Credentials

# Step 1: Load the service account JSON file
SERVICE_ACCOUNT_FILE = 'apikey2.json'  # Replace with your JSON file name
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Step 2: Authenticate with gspread
client = gspread.authorize(credentials)

# Step 3: Open the Google Sheet
spreadsheet_name = "hr-data-personal"  # Replace with the name of your spreadsheet
try:
    spreadsheet = client.open(spreadsheet_name)
    print(f"Successfully connected to the spreadsheet: {spreadsheet_name}")
    
    # Step 4: Select the first sheet
    worksheet = spreadsheet.sheet1
    
    # Step 5: Read data from the first row as a test
    first_row = worksheet.row_values(1)
    print(f"First row of data: {first_row}")
    
    # Step 6: Optionally, append a test row (remove if not needed)
    test_data = ["Test Department", "25", "Male", "10 km"]
    worksheet.append_row(test_data)
    print("Test data appended successfully!")
    
except Exception as e:
    print(f"An error occurred: {e}")