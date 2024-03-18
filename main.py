import streamlit as st  
from auth import run_auth_page 
from dashboard import run_dashboard 
from styles import apply_custom_css

def show_landing_page():
    apply_custom_css()
    st.title(" Welcome to DanBizInsight: Empowering Financial Insights")

    st.markdown("""
    Unlock the power of comprehensive financial analytics with [App Name]. Dive deep into sector performances, assess financial health at a glance, identify prime investment opportunities, analyze operational efficiency, and much more. Transform data into decisions with our advanced analysis tools designed for investors, analysts, and financial professionals.
    
    ### Sector Performance Overview
    
    Gain a macroeconomic perspective with our Sector Performance Overview. By analyzing key financial metrics like gross profit, equity, and assets across industries, DanBizInsight reveals which sectors are thriving and which face challenges. Track profitability trends, asset growth, and sector health over time, enabling informed strategic decisions.
    
    ### Financial Health Dashboard
    
    Evaluate company and sector financial health effortlessly with our intuitive dashboard. Key indicators such as solvency ratio, ROA, ROI, and current ratio are visualized for quick insights. Understand the financial foundations of potential investments and identify companies that stand on solid ground versus those at risk.
    
    ### Investment Opportunity Identification
    
    Discover attractive investment avenues with our analytical tools. DanBizInsight compares profit margins and ROI, alongside equity and asset growth, to spotlight companies poised for success. Filter opportunities that align with your investment strategy, backed by data-driven insights.
    
    ### Operational Efficiency Analysis
    
    Uncover the secrets behind operational success with our Operational Efficiency Analysis. Explore how companies convert efforts into profits by examining revenue, expenses, and operational profitability. Identify industry best practices and areas ripe for improvement, refining your operational strategies.
    
    ### Liquidity and Solvency Trend Analysis
    
    Navigate financial stability with our trend analysis features. Monitor liquidity and solvency through metrics like current ratio, solvency ratio, and cash reserves. Assess how well companies and sectors are positioned to meet obligations, ensuring your investments are secure.
    
    ### Capital Structure and Financing Insights
    
    Delve into the financial structures of companies with our comprehensive analysis tools. Understand how operations and growth are financed, whether through equity or debt, and the implications on financial stability and risk. Make informed decisions by analyzing capital structure dynamics.
    
    ### Get Started with DanBizInsight
    
    Embark on a journey of financial discovery. DanBizInsight equips you with the insights needed to navigate the complex world of finance with confidence. Start exploring today and transform data into actionable knowledge.
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.8, 0.2])  # Adjust the ratio to suit your layout needs

    with col2:  
        if st.button("Begin Exploration"):
            st.session_state['page'] = 'auth'
def main():
    apply_custom_css()
    # Initialize session state variables if they are not already set
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False 
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True  

    # Determine which page to display based on the session state
    if st.session_state.page == 'landing':
        show_landing_page()
    elif st.session_state.page == 'auth' and not st.session_state.logged_in:
        run_auth_page()
    elif st.session_state.logged_in:
        run_dashboard()

# Run the main function when the script is executed directly
if __name__ == "__main__":
    main()
