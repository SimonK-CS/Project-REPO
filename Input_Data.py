######Agenda######
# Step 0: Setting up the workplace incl. libraries/connecting API(i.e. workplace.py)
# Step 1: Creating the class which organizes the employees attributes
# Step 2: Defining the appending function which "appends" the entered data into the spreadsheet
# Step 3: Visualization Part that creates the form through Streamlit

# Step 00: Importing tools/libraries that are needed to perform different tasks
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Step 00: Setting up Google Sheets API

SERVICE_ACCOUNT_INFO = st.secrets["google_credentials"]
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# Login to read data from Google Sheets
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO, scopes=SCOPES
)

SAMPLE_SPREADSHEET_ID = '19CC438qwcEpCufbyukbzQ1RmVW9uZ1VK6rFHtXNU8IU'
SHEET_NAME = 'HR-Data'

#########################################################################################
# Step 1: Class that organizes employee attributes & converts employee data to list format
class EmployeeData:
    def __init__(self, department: str, age: int, gender: str, 
                 distance_from_home: int, education: str, job_role: str, 
                 marital_status: str, monthly_income: int, 
                 total_working_years: int):
        # Constructor to initialize employee data
        self.department = department
        self.age = age
        self.gender = gender
        self.distance_from_home = distance_from_home
        self.education = education
        self.job_role = job_role
        self.marital_status = marital_status
        self.monthly_income = monthly_income
        self.total_working_years = total_working_years
    
    def to_list(self) -> list:
        """Function that gathers all employee information and returns it as a list."""
        return [
            self.department, self.age, self.gender, self.distance_from_home,
            self.education, self.job_role, self.marital_status, 
            self.monthly_income, self.total_working_years
        ]

###########################################################################
# Step 2: Appending function to add the input data to the spreadsheet
def append_employee_data(employee: EmployeeData) -> bool:
    """Append the employee data to Google Sheets."""
    
    if isinstance(employee, EmployeeData):
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        request = sheet.values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SHEET_NAME,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={'values': [employee.to_list()]}
        )

        try:
            request.execute()
            return True
        except Exception as e:
            st.error(f"The request to append data failed: {e}")
            return False
    else:
        st.error("Employee data is in the wrong format")
        return False

################################################################
# Step 3: Visualize the Streamlit Form
st.title("Profile Manager")
st.subheader("Employee Data - Enter new Employee Information")

# Streamlit form for data input
with st.form("employee_data_form"):
    department = st.text_input("Department")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    distance_from_home = st.number_input("Distance from Home (km)", min_value=0, step=1)
    education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "Doctorate"])
    job_role = st.text_input("Job Role")
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
    monthly_income = st.number_input("Monthly Income ($)", min_value=1000, step=100)
    total_working_years = st.number_input("Total Working Years", min_value=0, step=1)

    # Submit Button
    submitted = st.form_submit_button("Submit")

# Adding the newly submitted input data into the class and appending it
if submitted:
    employee = EmployeeData(
        department=department,
        age=age,
        gender=gender,
        distance_from_home=distance_from_home,
        education=education,
        job_role=job_role,
        marital_status=marital_status,
        monthly_income=monthly_income,
        total_working_years=total_working_years
    )

    # Feedback
    if append_employee_data(employee):
        st.success("New employee successfully added")
    else:
        st.error("Failed to add employee data")