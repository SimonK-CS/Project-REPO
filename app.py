# Import necessary libraries
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt

# Google API authentication
key_file_path = "apikey2.json"  # JSON file with your API credentials
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]  # Read-only scope

credentials = Credentials.from_service_account_file(key_file_path, scopes=scopes)
client = gspread.authorize(credentials)

# Load Google Sheet and fetch data
sheet = client.open("HR-Data").worksheet("HR-Data1")  # Open the specific Google Sheet and worksheet
range_data = sheet.get("A1:AI1471")  # Fetch the specific range

# Convert the range data into a DataFrame
df = pd.DataFrame(range_data[1:], columns=range_data[0])  # Use the first row as header and the rest as data

# Streamlit app
st.title("Google Sheets Data Visualization in Streamlit")

# Display the dataset
st.subheader("Dataset")
st.write(df)

# First visualization: Pie chart (Department Distribution)
st.subheader("Percentage of Employees by Department")
department_counts = df['Department'].value_counts()  # Count occurrences in the 'Department' column
percentages = department_counts / department_counts.sum() * 100  # Calculate percentages

# Create pie chart
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.pie(percentages, labels=percentages.index, autopct='%1.1f%%', startangle=140)
ax1.set_title('Percentage of Employees by Department')
ax1.axis('equal')  # Ensures the pie chart is a circle
st.pyplot(fig1)