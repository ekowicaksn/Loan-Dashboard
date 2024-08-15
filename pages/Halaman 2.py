import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Demo Sashboard",page_icon='🎨',layout='wide')
st.title("Financial Insights Dashboard: Loan Performance & Trends")
st.markdown("---")
st.sidebar.header('Dashboard Filters and Features')
st.sidebar.markdown('''
                    - **Overview**: Provides a summary of key loan metrics.
                    - **Time-Based Analysis**: Shows trends over time and loan amounts.
                    - **Loan Performance**: Analyzes loan conditions and distributions.
                    - **Financial Analysis**: Examines loan amounts and distributions based on conditions.'''
                    )
loan=pd.read_pickle('data_input/loan_clean')
loan['purpose']=loan['purpose'].str.replace("_"," ")

st.subheader("Analysis")
condition=st.selectbox("Select Loan Condition",["Good Loan",'Bad Loan'])
loan_condition=loan[loan['loan_condition']==condition]
with st.container(border=True): #ngasih border
        tab4, tab5=st.tabs(['**Loan Amount Distribution**','**Loan Amount Distribution by Purpose**']) 
with tab4:
        histo_term=px.histogram(loan_condition,x='loan_amount',nbins=20,color='term',template='seaborn',labels={
        'loan_amount':'Loan Amount',
        'term':'Loan Term'})
        st.plotly_chart(histo_term)
with tab5:
        grade = loan['grade'].value_counts().sort_index()
        boxplot_termpurpose=px.box(loan_condition,x='purpose',y='loan_amount',color='term',template='seaborn',
        labels={'purpose':'Loan Purpose','loan_amount':'Loan Amount','term':'Term'},title='Loan Amount by Purpose & Term')
        st.plotly_chart(boxplot_termpurpose)