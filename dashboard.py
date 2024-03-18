# Import the required libraries and modules
import streamlit as st  # Used for creating the web app interface
import sqlite3  # Used for SQLite database operations
import plotly.express as px  # Used for creating interactive charts
import pandas as pd  # Used for data manipulation and analysis
from styles import apply_custom_css  # Custom function to apply CSS styling
import os  
from utils import sector_attributes, get_company_codes
from metrics import sector_performance_overview, financial_health_dashboard, investment_opportunity_identification, company_level_comparison, visualize_company_comparison, operational_efficiency_analysis, liquidity_and_solvency_trend_analysis
from db import get_year_range, get_sector_choices, fetch_companies_in_sector, fetch_company_financial_history, fetch_financial_data_for_two_companies, display_company_info


# Main function to run the Streamlit dashboard
def run_dashboard():
    # Apply custom CSS styles to the Streamlit app
    apply_custom_css()
    st.sidebar.header("Filters")
    # Retrieve and display sector choices in the sidebar
    sectors = get_sector_choices()
    sector_choice = st.sidebar.selectbox("Select Sector", sectors, format_func=lambda x: sector_attributes.get(x, x))

    # Get the available year range from the database
    min_year, max_year = get_year_range()
    # Allow the user to select a start year within the range
    start_year = st.sidebar.text_input("Start Year", value=str(min_year))
    # Allow the user to select an end year within the range
    end_year = st.sidebar.text_input("End Year", value=str(max_year))

    # Attempt to convert the selected year range to integers
    try:
        selected_start_year = int(start_year)
        selected_end_year = int(end_year)
    except ValueError:
        # Display an error message if the conversion fails and revert to the full range
        st.sidebar.error("Please enter valid years")
        selected_start_year, selected_end_year = min_year, max_year

    # Display the main header for the dashboard
    st.header("Investor Dashboard")
    # Create a sidebar selection box for different data views
    view_data = st.sidebar.selectbox("View Data", ["Sector Performance Overview","Financial Health Dashboard", "Investment Opportunity Identification", "Company Comparison", "Operational Efficiency Analysis", "Liquidity and Solvency Trend Analysis", "Capital Structure and Financing Insights", "Company Analysis", "Company to Company Comparison", "Company Information"])

    sector_code = get_company_codes(sector_choice)
    if view_data == "Sector Performance Overview":
        sector_performance_overview()
    elif view_data == "Financial Health Dashboard":
        # once clicked show a select box
        more_data = st.sidebar.selectbox("Select Financial Health Metrics", ['Average Solvency Ratio by Sector Over Time', 'Average ROA by Sector Over Time', 'Average ROI by Sector Over Time', 'Average Current Ratio by Sector Over Time'])
        # call financial health dashboard function with an argument depending on the selection
        if more_data == 'Average Solvency Ratio by Sector Over Time':
            financial_health_dashboard('avg_solvency_ratio')
        elif more_data == 'Average ROA by Sector Over Time':
            financial_health_dashboard('avg_return_on_assets')
        elif more_data == 'Average ROI by Sector Over Time':
            financial_health_dashboard('avg_return_on_investment')
        elif more_data == 'Average Current Ratio by Sector Over Time':
            financial_health_dashboard('avg_current_ratio')
    elif view_data == "Investment Opportunity Identification":
        investment_opportunity_identification()
    elif view_data == "Operational Efficiency Analysis":
        operational_efficiency_analysis()
    elif view_data == "Liquidity and Solvency Trend Analysis":
        liquidity_and_solvency_trend_analysis()
    elif view_data == "Company Analysis":
        # Fetch and display a list of companies in the selected sector for analysis
        companies = fetch_companies_in_sector(sector_code)
        if companies:
            # Allow the user to select a company from the list for analysis
            selected_company = st.sidebar.selectbox("Select a Company for Analysis", companies, format_func=lambda x: x[1])
            # Extract the CVR number of the selected company
            cvr_number = selected_company[0]
            
            # Display financial data for the selected company when the user clicks the 'Show Financial Data' button
            if st.sidebar.button('Show Financial Data'):
                company_data = fetch_company_financial_history(cvr_number, (selected_start_year, selected_end_year))
                if company_data:
                    # Convert the fetched data into a DataFrame
                    df = pd.DataFrame(company_data, columns=['Year', 'Profit/Loss (DKK)', 'Equity', 'ROA'])
                    
                    # Create and display a line chart for the company's profit/loss history
                    profit_loss_fig = px.line(df, x='Year', y='Profit/Loss (DKK)', title=f'Profit/Loss of {selected_company[1]}')
                    st.plotly_chart(profit_loss_fig, use_container_width=True)

                    # Create and display a line chart for the company's equity history
                    equity_fig = px.line(df, x='Year', y='Equity', title=f'Equity of {selected_company[1]}')
                    st.plotly_chart(equity_fig, use_container_width=True)

                    # Create and display a line chart for the company's ROA history
                    roa_fig = px.line(df, x='Year', y='ROA', title=f'Return on Assets (ROA) of {selected_company[1]}')
                    st.plotly_chart(roa_fig, use_container_width=True)
                    
                    # Display a detailed explanation of the company's financial analysis
                    st.markdown(f"""
                    The financial analysis of **{selected_company[1]}** shows the annual Profit/Loss (DKK), Equity, and Return on Assets (ROA). These metrics are crucial for assessing the company's financial health and operational efficiency.
                
                    - **Profit/Loss** provides insight into the company's profitability and financial performance.
                    - **Equity** indicates the company's net value, reflecting its financial stability.
                    - **ROA** measures how efficiently the company's assets are used to generate profit.
                    
                    This comprehensive financial overview helps in making informed investment decisions.
                    """)   
                else:
                    # Display a message if no financial data is available for the selected company
                    st.write("No financial data available for the selected company.")
                
    elif view_data == "Company to Company Comparison":
        # Fetch and display a list of companies in the selected sector for comparison
        companies = fetch_companies_in_sector(sector_code)
        if companies:
            # Create a list of company options for comparison
            company_options = [(cvr, name) for cvr, name in companies]
            # Allow the user to select the first company for comparison
            cvr_number1, company_name1 = st.sidebar.selectbox("Select the first company for comparison", company_options, format_func=lambda x: x[1])
            # Allow the user to select the second company for comparison
            cvr_number2, company_name2 = st.sidebar.selectbox("Select the second company for comparison", company_options, format_func=lambda x: x[1])

            # Display comparison data when the user clicks the 'Compare Companies' button
            if st.sidebar.button('Compare Companies'):
                comparison_data = fetch_financial_data_for_two_companies(cvr_number1, cvr_number2, (selected_start_year, selected_end_year))
                if comparison_data:
                    # Convert the fetched data into a DataFrame and add a 'Company' column for identification
                    df = pd.DataFrame(comparison_data, columns=['CVR', 'Year', 'Profit/Loss (DKK)', 'Equity', 'ROA'])
                    df['Company'] = df['CVR'].map({cvr_number1: company_name1, cvr_number2: company_name2})
                    
                    # Create and display bar charts for financial comparison between the two companies
                    for metric in ['Profit/Loss (DKK)', 'Equity', 'ROA']:
                        fig = px.bar(df, x='Company', y=metric, barmode='group', color='Company', title=f'{metric} Comparison for {company_name1} vs {company_name2}')
                        fig.update_xaxes(title_text='Company')
                        fig.update_yaxes(title_text=metric)
                        st.plotly_chart(fig, use_container_width=True)
                        
                    # Display a detailed explanation of the company-to-company financial comparison
                    st.markdown(f"""
                    Comparing **{company_name1}** and **{company_name2}** provides a side-by-side view of their financial performance. This comparison includes Profit/Loss, Equity, and Return on Assets (ROA), key metrics that highlight each company's financial strengths and weaknesses.
                    - **Profit/Loss** comparison reveals which company is more profitable.
                    - **Equity** comparison shows the financial stability and net value of each company.
                    - **ROA** comparison indicates how effectively each company uses its assets to generate profit.
                    
                    This information aids in making strategic investment decisions, identifying which company presents a better financial profile.
                    """)
                else:
                    # Display a message if no data is available for the selected companies
                    st.write("No data available for the selected companies.")
                    
    elif view_data == "Company Information":
        # Fetch and display a list of companies in the selected sector for information viewing
        companies = fetch_companies_in_sector(sector_code)
        if companies:
            # Create a list of company options for information viewing
            company_options = [(cvr, name) for cvr, name in companies]
            # Allow the user to select a company for viewing its information
            selected_company = st.sidebar.selectbox("Select a company", company_options, format_func=lambda x: x[1], key="company_info")
            # Extract the CVR number of the selected company
            selected_cvr = selected_company[0]

            # Display the information for the selected company
            display_company_info(selected_cvr)
        else:
            # Display a message if no companies are available in the selected sector
            st.write("No companies available in the selected sector.")

    else:
        st.write("Hello world")

    # add logout button
    if st.sidebar.button("Logout"):
        st.session_state.show_login = True
        st.session_state.logged_in = False