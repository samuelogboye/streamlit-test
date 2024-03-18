import pandas as pd
import streamlit as st
from utils import sector_attributes
from db import get_db_connection
import plotly.express as px

# @st.cache_data(suppress_st_warning=True) 
def sector_performance_overview():
    # Establish a connection to the database
    conn = get_db_connection()
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    # SQL query to select data from the 'financials' table
    query = """
        SELECT c.industry_sector, f.year, AVG(f.gross_profit_loss) AS avg_gross_profit_loss, 
               AVG(f.equity) AS avg_equity, AVG(f.assets) AS avg_assets
        FROM financials f
        JOIN company c ON f.cvr = c.cvr_number
        GROUP BY c.industry_sector, f.year
        ORDER BY c.industry_sector, f.year;
        """

    df_sector_performance = pd.read_sql_query(query, conn)

    # Map sector codes to names
    df_sector_performance['industry_sector'] = df_sector_performance['industry_sector'].replace(sector_attributes)

    fig = px.line(df_sector_performance, x='year', y='avg_equity', color='industry_sector',
              title='Average Equity by Sector Over Time')
    
    fig.update_layout(width=1200)
    st.plotly_chart(fig)


# @st.cache_data(suppress_st_warning=True) 
def financial_health_dashboard(metric):
    # Establish a connection to the database
    conn = get_db_connection()
    
    # SQL query to fetch financial health indicators
    query = """
    SELECT c.industry_sector, f.year,
           AVG(f.solvency_ratio) AS avg_solvency_ratio,
           AVG(f.return_on_assets) AS avg_return_on_assets,
           AVG(f.return_on_investment) AS avg_return_on_investment,
           AVG(f.current_ratio) AS avg_current_ratio
    FROM financials f
    JOIN company c ON f.cvr = c.cvr_number
    GROUP BY c.industry_sector, f.year
    ORDER BY c.industry_sector, f.year;
    """

    # Execute the query and load the data into a DataFrame
    df_financial_health = pd.read_sql_query(query, conn)

    # Map sector codes to names using the previously defined `sector_attributes`
    df_financial_health['industry_sector'] = df_financial_health['industry_sector'].replace(sector_attributes)

    # Ensure correct data types
    df_financial_health['year'] = pd.to_datetime(df_financial_health['year'], format='%Y')

    # Create the dashboard visualizations
    create_financial_health_charts(df_financial_health, metric)



def create_financial_health_charts(df, metric):
    # Solvency Ratio
    fig_solvency = px.line(df, x='year', y='avg_solvency_ratio', color='industry_sector',
                           title='Average Solvency Ratio by Sector Over Time')
    fig_solvency.update_layout(width=1200, height=600)

    # Return on Assets
    fig_roa = px.line(df, x='year', y='avg_return_on_assets', color='industry_sector',
                      title='Average Return on Assets by Sector Over Time')
    fig_roa.update_layout(width=1200, height=600)

    # Return on Investment
    fig_roi = px.line(df, x='year', y='avg_return_on_investment', color='industry_sector',
                      title='Average Return on Investment by Sector Over Time')
    fig_roi.update_layout(width=1200, height=600)

    # Current Ratio
    fig_current_ratio = px.line(df, x='year', y='avg_current_ratio', color='industry_sector',
                                title='Average Current Ratio by Sector Over Time')
    fig_current_ratio.update_layout(width=1200, height=600)

    # Use Streamlit to layout the charts on the page
    if metric == 'avg_solvency_ratio':
        st.plotly_chart(fig_solvency)
    elif metric == 'avg_return_on_assets':
        st.plotly_chart(fig_roa)
    elif metric == 'avg_return_on_investment':
        st.plotly_chart(fig_roi)
    elif metric == 'avg_current_ratio':
        st.plotly_chart(fig_current_ratio)


def investment_opportunity_identification():
    # Establish a connection to the database
    conn = get_db_connection()
    
    # SQL query to fetch necessary financial data for each company over the years
    query = """
    SELECT c.name AS company_name, c.industry_sector, f.year,
           f.profit_margin, f.return_on_investment, f.equity, f.assets
    FROM financials f
    JOIN company c ON f.cvr = c.cvr_number
    ORDER BY c.name, f.year;
    """

    # Execute the query and load the data into a DataFrame
    df_investment_opportunities = pd.read_sql_query(query, conn)

    # Map sector codes to names using the `sector_attributes` defined earlier
    df_investment_opportunities['industry_sector'] = df_investment_opportunities['industry_sector'].replace(sector_attributes)

    # Calculate year-over-year growth for equity and assets
    df_investment_opportunities['equity_growth'] = df_investment_opportunities.groupby('company_name')['equity'].pct_change()
    df_investment_opportunities['assets_growth'] = df_investment_opportunities.groupby('company_name')['assets'].pct_change()

    # Filter companies showing consistent increase in metrics (customize the threshold as needed)
    df_filtered = df_investment_opportunities[
        (df_investment_opportunities['profit_margin'] > 0) &
        (df_investment_opportunities['return_on_investment'] > 0) &
        (df_investment_opportunities['equity_growth'] > 0) &
        (df_investment_opportunities['assets_growth'] > 0)
    ]

    # Visualize the filtered data
    visualize_investment_opportunities(df_filtered)


def visualize_investment_opportunities(df):
    # Customize this visualization based on the insights you wish to highlight
    # Example: Scatter plot comparing Return on Investment and Profit Margin for the latest year available
    
    # Assuming 'df' is filtered to include only the latest year for each company
    fig = px.scatter(df, x='return_on_investment', y='profit_margin', color='industry_sector',
                     hover_data=['company_name', 'equity_growth', 'assets_growth'],
                     title='Investment Opportunities: ROI vs. Profit Margin')
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)

@st.cache_resource
def company_level_comparison():
    # Establish a connection to the database
    conn = get_db_connection()
    
    # SQL query to fetch necessary financial data for each company over the years
    query = """
    SELECT c.name AS company_name, c.industry_sector, f.year,
           f.profit_margin, f.return_on_investment, f.equity, f.assets
    FROM financials f
    JOIN company c ON f.cvr = c.cvr_number
    ORDER BY c.name, f.year;
    """

    # Execute the query and load the data into a DataFrame
    df_company_comparison = pd.read_sql_query(query, conn)

    # Map sector codes to names
    df_company_comparison['industry_sector'] = df_company_comparison['industry_sector'].replace(sector_attributes)

    # Calculate year-over-year growth for equity and assets
    df_company_comparison['equity_growth'] = df_company_comparison.groupby('company_name')['equity'].pct_change()
    df_company_comparison['assets_growth'] = df_company_comparison.groupby('company_name')['assets'].pct_change()

    return df_company_comparison


def visualize_company_comparison(df):
    # Handle NaN values by filling with 0 or a small positive value
    df['equity_growth'] = df['equity_growth'].fillna(0)
    
    # Adjust negative values if needed, here we're taking the absolute value
    df['equity_growth'] = df['equity_growth'].abs()
    
#     # Optional: Normalize or scale the 'equity_growth' values to a suitable range for visualization
#     # For example, scaling to a range between 10 and 100
#     from sklearn.preprocessing import MinMaxScaler
#     scaler = MinMaxScaler(feature_range=(10, 100))
#     df['equity_growth_scaled'] = scaler.fit_transform(df[['equity_growth']])
    # Then, normalize 'equity_growth' to a 0-1 range
    equity_growth_min = df['equity_growth'].min()
    equity_growth_max = df['equity_growth'].max()
    df['equity_growth_normalized'] = (df['equity_growth'] - equity_growth_min) / (equity_growth_max - equity_growth_min)
    
    # Finally, scale to your desired range, for example, 10 to 100
    min_size = 10
    max_size = 100
    df['equity_growth_scaled'] = df['equity_growth_normalized'] * (max_size - min_size) + min_size
        
    fig = px.scatter(df, x='return_on_investment', y='profit_margin', 
                     size='equity_growth_scaled', color='company_name', 
                     hover_data=['company_name', 'equity_growth', 'assets_growth'],
                     title='Company-Level Comparison: ROI vs. Profit Margin with Equity Growth')
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)


def operational_efficiency_analysis():
    # Establish a connection to the database
    conn = get_db_connection()
    
    # SQL query to fetch necessary financial data
    query = """
    SELECT c.name AS company_name, f.year,
           f.revenue, f.external_expenses, f.employee_expense, 
           f.profit_loss_from_ordinary_operating_activities
    FROM financials f
    JOIN company c ON f.cvr = c.cvr_number
    ORDER BY c.name, f.year;
    """

    # Execute the query and load the data into a DataFrame
    df_efficiency = pd.read_sql_query(query, conn)

    # Calculate operational efficiency metrics
    df_efficiency['operating_margin'] = df_efficiency['profit_loss_from_ordinary_operating_activities'] / df_efficiency['revenue']
    df_efficiency['expense_ratio'] = (df_efficiency['external_expenses'] + df_efficiency['employee_expense']) / df_efficiency['revenue']

    # Visualization
    visualize_operational_efficiency(df_efficiency)


def visualize_operational_efficiency(df):
    # Operating Margin Over Time for Each Company
    fig_margin = px.line(df, x='year', y='operating_margin', color='company_name', 
                         title='Operating Margin Over Time by Company')
    fig_margin.update_layout(width=1000, height=600)
    st.plotly_chart(fig_margin)

    # Expense Ratio Over Time for Each Company
    fig_expense_ratio = px.line(df, x='year', y='expense_ratio', color='company_name', 
                                title='Expense Ratio Over Time by Company')
    fig_expense_ratio.update_layout(width=1000, height=600)
    st.plotly_chart(fig_expense_ratio)


def liquidity_and_solvency_trend_analysis():
    # Establish a connection to the database
    conn = get_db_connection()
    
    # SQL query to fetch liquidity and solvency data
    query = """
    SELECT c.name AS company_name, f.year,
           f.current_ratio, f.solvency_ratio, f.cash_and_cash_equivalents
    FROM financials f
    JOIN company c ON f.cvr = c.cvr_number
    ORDER BY c.name, f.year;
    """

    # Execute the query and load the data into a DataFrame
    df_liquidity_solvency = pd.read_sql_query(query, conn)

    # Visualization
    visualize_liquidity_and_solvency(df_liquidity_solvency)

    conn.close()

def visualize_liquidity_and_solvency(df):
    # Current Ratio Over Time for Each Company
    fig_current_ratio = px.line(df, x='year', y='current_ratio', color='company_name', 
                                title='Current Ratio Over Time by Company')
    fig_current_ratio.update_layout(width=1000, height=600)
    st.plotly_chart(fig_current_ratio)

    # Solvency Ratio Over Time for Each Company
    fig_solvency_ratio = px.line(df, x='year', y='solvency_ratio', color='company_name', 
                                 title='Solvency Ratio Over Time by Company')
    fig_solvency_ratio.update_layout(width=1000, height=600)
    st.plotly_chart(fig_solvency_ratio)

    # Cash and Cash Equivalents Over Time for Each Company
    fig_cash = px.line(df, x='year', y='cash_and_cash_equivalents', color='company_name', 
                       title='Cash and Cash Equivalents Over Time by Company')
    fig_cash.update_layout(width=1000, height=600)
    st.plotly_chart(fig_cash)
