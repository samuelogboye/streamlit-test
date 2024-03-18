import sqlite3
import os
from utils import sector_attributes
import streamlit as st


# Function to establish a connection with the SQLite database
def get_db_connection():
    # Build the path to the database file using the current file location
    db_path = os.path.join(os.path.dirname(__file__), 'cvr_database.db')
    # Connect to the SQLite database and return the connection object
    return sqlite3.connect(db_path)

# Function to set up the database by creating necessary tables if they don't exist
def setup_database():
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # SQL query to check if the 'users' table exists in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    # Fetch the result of the query
    table_exists = cursor.fetchone()

    # Uncomment below lines to drop the 'users' table if it exists (optional, based on requirements)
    # if table_exists:
    #     cursor.execute("DROP TABLE users")

    # SQL query to create the 'users' table if it does not already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            sectors TEXT
        )
    """)
    # Commit the changes to the database
    conn.commit()

def get_sector_choices():
    return list(sector_attributes.values())


# Function to get the range of years from the 'financials' table in the database
def get_year_range():
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # Execute a SQL query to find the minimum and maximum year in the 'financials' table
    cursor.execute("SELECT MIN(year), MAX(year) FROM financials")
    # Fetch the result of the query
    min_year, max_year = cursor.fetchone()
    # Return the minimum and maximum year
    return min_year, max_year

def fetch_companies_in_sector(sector_code):
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # SQL query to select companies from a specific sector, ordered by name
    query = """
    SELECT cvr_number, name
    FROM company
    WHERE industry_sector = ?
    ORDER BY name
    """
    # Execute the query with the sector_code as a parameter
    cursor.execute(query, (sector_code,))
    # Fetch all rows of the query result
    return cursor.fetchall()

def fetch_company_financial_history(cvr_number, year_range):
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # SQL query to select year, profit/loss, equity, and return on assets for the given company and year range
    query = """
    SELECT year, profit_loss, equity, return_on_assets
    FROM financials
    WHERE cvr = ? AND year BETWEEN ? AND ?
    ORDER BY year
    """
    # Combine the CVR number and year range into a single tuple for the query parameters
    params = (cvr_number,) + year_range
    # Execute the query with the parameters
    cursor.execute(query, params)
    # Fetch all rows of the query result
    return cursor.fetchall()

# Function to display detailed information for a selected company using its CVR number
def display_company_info(cvr_number):
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # SQL queries to select basic and financial information for the given company
    company_query = "SELECT name, industry_sector, email, phone_number, establishment_date, purpose FROM company WHERE cvr_number = ?"
    financial_query = "SELECT profit_loss, equity, return_on_assets, solvency_ratio FROM financials WHERE cvr = ? ORDER BY year DESC LIMIT 1"
    
    # Execute the queries
    cursor.execute(company_query, (cvr_number,))
    company_data = cursor.fetchone()
    
    cursor.execute(financial_query, (cvr_number,))
    financial_data = cursor.fetchone()
    
    # Check and display company data if available
    if company_data:
        # Unpack the company data into variables
        name, sector, email, phone, establishment_date, purpose = company_data
        # Display company information using Streamlit functions
        st.subheader(f'Company Information')
        st.markdown(f"**Company Name:** {name or 'Not provided'}")
        st.markdown(f"**Sector:** {sector_attributes.get(sector, 'Unknown Sector')}")
        st.markdown(f"**Establishment Date:** {establishment_date or 'Not available'}")
        st.markdown(f"**Company Purpose:** {purpose or 'Not provided'}")
        st.markdown(f"**Email:** {email or 'Not provided'}")
        st.markdown(f"**Phone Number:** {phone or 'Not provided'}")
    else:
        # Display error message if company data is not available
        st.error("Company information not available.")
    
    # Check and display financial data if available
    if financial_data:
        # Unpack the financial data into variables
        profit_loss, equity, roa, solvency_ratio = financial_data
        # Display financial information using Streamlit functions
        st.subheader("Financial Information (Most Recent Year)")
        st.metric("Profit/Loss", f"{profit_loss} DKK")
        st.metric("Equity", f"{equity} DKK")
        st.metric("Return on Assets", f"{roa * 100}%", delta_color="off")
        st.metric("Solvency Ratio", f"{solvency_ratio * 100}%", delta_color="off")
    else:
        # Display error message if financial data is not available
        st.error("Financial information not available.")

def fetch_financial_data_for_two_companies(cvr_number1, cvr_number2, year_range):
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # SQL query to select financial data for two companies over the given year range
    query = """
    SELECT cvr, year, profit_loss, equity, return_on_assets
    FROM financials
    WHERE cvr IN (?, ?) AND year BETWEEN ? AND ?
    ORDER BY year, cvr
    """
    # Combine the parameters into a single tuple
    params = (cvr_number1, cvr_number2, year_range[0], year_range[1])
    # Execute the query with the parameters
    cursor.execute(query, params)
    # Fetch all rows of the query result
    return cursor.fetchall()