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

with st.container(border=True): #ngasih border
    col1, col2=st.columns(2) #mendefinisikan nama kolom, block abis itu teken tab
    with col1:
        st.metric('💡**Total Loans**',(f"{loan['id'].count():,.0f}"), help='Total Number of Loans')
        st.metric('💡**Total Loan Amount**',(f"${loan['loan_amount'].sum():,.0f}"),help='Total Loan Amount')
    with col2:
        st.metric('💡**Average Interest Rate**',(f"{loan['interest_rate'].mean():,.2f}%"),help='Average Interest Rate')
        st.metric('💡**Average Loan Amount**',(f"${loan['loan_amount'].mean():,.0f}"),help='Average Loan Amount')

with st.container(border=True): #ngasih border
    tab1,tab2,tab3 = st.tabs(['**Loan Issued Over Time**','**Loan Amount Over Time**','**Issue Date Analysis**'])
    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
        line_count=px.line(
            loan_date_count,markers=True,
            title="Number of Loan Issued Over Time", 
            labels={'issue_date':'Issue Date','value':'Number of Loans'},
            template='seaborn'
        ).update_layout(showlegend=False)
        st.plotly_chart(line_count)
    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        line_sum=px.line(loan_date_sum,markers=True,
            title="Number of Loan Amount Over Time",
            labels={'issue_date':'Issue Date','value':'Amount of Loans'},
            template='seaborn').update_layout(showlegend=False)
        st.plotly_chart(line_sum)
    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        line_day=px.bar(loan_day_count,category_orders={'issue_weekday':['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']},
            title="Distribution of Loans by Day Issuance",
            labels={'issue_weekday':'Day of Issuance','value':'Number of Loans'},
            template='seaborn').update_layout(showlegend=False)
        st.plotly_chart(line_day)

st.subheader("Loan Condition")
with st.expander(''): #expande/collapse column
    col3, col4=st.columns(2) #mendefinisikan nama kolom, block abis itu teken tab
    with col3:
        pie_grade=px.pie(loan,title='Loan Portion by Grade',names='loan_condition',hole=0.4,template='seaborn').update_traces(textinfo='percent+value')
        st.plotly_chart(pie_grade)
    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar_grade=px.bar(grade,
            title= "Distribution of Loans by Grade",
            labels={'grade' : "Grade",'value' : "Number of Loans"},template='seaborn').update_layout(showlegend = False)
        st.plotly_chart(bar_grade)

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