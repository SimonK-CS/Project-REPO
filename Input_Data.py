###Level 8: Some nice styling###
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Streamlit App Title
st.set_page_config(page_title="HR Nexus", layout="wide")  # Wide layout for better spacing

# Authenticate the Google Sheets API
SERVICE_ACCOUNT_FILE = 'apikey2.json'
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

# Open Google Sheet
spreadsheet_name = "HR-Data-Personal"
spreadsheet = client.open(spreadsheet_name)
worksheet = spreadsheet.sheet1

# Get headers and all data
headers = worksheet.row_values(1)
sheet_data = worksheet.get_all_values()

# Navigation state
if "page" not in st.session_state:
    st.session_state.page = "main"  # Default to main page
if "bg_color" not in st.session_state:
    st.session_state.bg_color = "#FFFFFF"  # Default background color

# Set background color
st.markdown(
    f"""
    <style>
    .main {{
        background-color: {st.session_state.bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load images
image_1 = "Main_Page_1.png"  # Replace with your first image file path
image_2 = "Main_Page_2.png"  # Replace with your second image file path


# Main Page
def main_page():
    st.header("Welcome to HR Nexus")
    st.write("Your one-stop solution for efficient employee management!")

    # Display images horizontally
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image(image_1, caption="Manage Employee Data", use_column_width=True)
    with col2:
        st.image(image_2, caption="Track Employee Performance", use_column_width=True)

    # Arrange buttons horizontally with creative names and colors
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎉 Onboard New Talent"):
            st.session_state.page = "add_employee"
            st.session_state.bg_color = "#D3D3D3"  # Light gray for Add Employee page
    with col2:
        if st.button("✏️ Edit Employee Records"):
            st.session_state.page = "change_employee"
            st.session_state.bg_color = "#C8AD7F"  # Beige for Change Employee page
    with col3:
        if st.button("🗑️ Farewell an Employee"):
            st.session_state.page = "delete_employee"
            st.session_state.bg_color = "#F5A9A9"  # Light red for Delete Employee page

    # Add a motivational quote
    st.markdown(
        """
        <blockquote style="text-align: center; font-style: italic; margin-top: 20px;">
        "It’s the job that’s never started as takes longest to finish." - Sam Gamgee
        </blockquote>
        """,
        unsafe_allow_html=True
    )


# Add New Employee Page
def add_employee_page():
    # Place return button at the top right
    st.markdown("<div style='text-align: right'>", unsafe_allow_html=True)
    if st.button("🏠 Return to Home Page"):
        st.session_state.page = "main"
    st.markdown("</div>", unsafe_allow_html=True)

    st.header("🎉 Onboard New Talent")
    st.write("Enter details for the new employee:")

    # Find the next available Employee Number
    employee_numbers = [int(row[headers.index("EmployeeNumber")]) for row in sheet_data[1:] if row[headers.index("EmployeeNumber")].isdigit()]
    next_employee_number = max(employee_numbers, default=0) + 1

    # Employee input form
    with st.form("add_employee_form"):
        age = st.selectbox("Age", list(range(18, 63)))
        attrition = st.selectbox("Attrition", ["Yes", "No"])
        business_travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
        daily_rate = st.number_input("Daily Rate", min_value=0, step=1)
        department = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
        distance_from_home = st.number_input("Distance from Home (km)", min_value=0, step=1)
        education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "Doctorate"])
        education_field = st.text_input("Education Field")
        employee_count = st.number_input("Employee Count", min_value=1, step=1)
        employee_number = st.number_input("Employee Number", min_value=next_employee_number, value=next_employee_number, step=1)
        environment_satisfaction = st.slider("Environment Satisfaction", min_value=1, max_value=4)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        hourly_rate = st.number_input("Hourly Rate", min_value=0, step=1)
        job_involvement = st.slider("Job Involvement", min_value=1, max_value=4)
        job_level = st.number_input("Job Level", min_value=1, step=1)
        job_role = st.text_input("Job Role")
        job_satisfaction = st.slider("Job Satisfaction", min_value=1, max_value=4)
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, step=100)
        monthly_rate = st.number_input("Monthly Rate", min_value=1000, step=100)
        num_companies_worked = st.number_input("Number of Companies Worked", min_value=0, step=1)
        over_18 = st.selectbox("Over 18", ["Yes", "No"])
        overtime = st.selectbox("Overtime", ["Yes", "No"])
        percent_salary_hike = st.slider("Percent Salary Hike", min_value=0, max_value=100)
        performance_rating = st.slider("Performance Rating", min_value=1, max_value=5)
        relationship_satisfaction = st.slider("Relationship Satisfaction", min_value=1, max_value=4)
        standard_hours = st.number_input("Standard Hours", min_value=1, step=1)
        stock_option_level = st.number_input("Stock Option Level", min_value=0, step=1)
        total_working_years = st.number_input("Total Working Years", min_value=0, step=1)
        training_times_last_year = st.number_input("Training Times Last Year", min_value=0, step=1)
        work_life_balance = st.slider("Work-Life Balance", min_value=1, max_value=4)
        years_at_company = st.number_input("Years at Company", min_value=0, step=1)
        years_in_current_role = st.number_input("Years in Current Role", min_value=0, step=1)
        years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, step=1)
        years_with_curr_manager = st.number_input("Years with Current Manager", min_value=0, step=1)

        # Submit button
        if st.form_submit_button("Submit"):
            new_employee = [
                age, attrition, business_travel, daily_rate, department, distance_from_home,
                education, education_field, employee_count, employee_number, environment_satisfaction,
                gender, hourly_rate, job_involvement, job_level, job_role, job_satisfaction, marital_status,
                monthly_income, monthly_rate, num_companies_worked, over_18, overtime, percent_salary_hike,
                performance_rating, relationship_satisfaction, standard_hours, stock_option_level,
                total_working_years, training_times_last_year, work_life_balance, years_at_company,
                years_in_current_role, years_since_last_promotion, years_with_curr_manager
            ]
            worksheet.append_row(new_employee)
            st.success(f"Employee added successfully with Employee Number {employee_number}!")

# Navigation Logic
if st.session_state.page == "main":
    main_page()
elif st.session_state.page == "add_employee":
    add_employee_page()
