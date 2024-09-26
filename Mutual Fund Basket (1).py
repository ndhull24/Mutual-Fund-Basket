#!/usr/bin/env python
# coding: utf-8

# In[27]:


import pandas as pd
df = pd.read_csv(r"C:\Users\Navdeep\Desktop\Self Machine Learning\Mutual Fund project\nifty50_closing_prices.csv")


# In[3]:


df.head()


# In[4]:


df.shape


# In[5]:


#Convert the date column into a datetime data type:
df['Date']= pd.to_datetime(df['Date'])


# In[6]:


df.isnull().sum()


# In[7]:


df.fillna(method='ffill', inplace=True)


# In[8]:


#Plotting the stock price to check the trend
import plotly.graph_objs as go
import plotly.express as px


# In[9]:


fig = go.Figure()

for company in df.columns[1:]:
    fig.add_trace(go.Scatter(x=df['Date'], y=df[company], mode= 'lines', name= company, opacity = 0.5))
    
fig.update_layout(
title = 'Stock Price Trends of All Indian Companies', 
xaxis_title = 'Date', yaxis_title = 'Closing Price (INR)', xaxis= dict(tickangle= 45),
legend = dict(x=1.05, y = 1, traceorder= 'normal', font= dict(size=10), 
             orientation= 'v'),
margin = dict(l=0, r=0, t= 30, b= 0), hovermode= 'x', template = 'plotly_white')

fig.show()


# Q. Which are the companies with hight risk?

# In[10]:


all_companies = df.columns[1:]

volatility_all_companies = df[all_companies].std()

volatility_all_companies.sort_values(ascending = False).head(10)


# Q. Which are the companies with highest growth rate?

# In[12]:


growth_all_companies = df[all_companies].pct_change()*100

avg_growth_all_companies = growth_all_companies.mean()

avg_growth_all_companies.sort_values(ascending= False).head(10)


# Companies with highest return on investments?

# In[15]:


initial_price_all= df[all_companies].iloc[0]

final_price_all = df[all_companies].iloc[-1]

roi_all_companies = ((final_price_all- initial_price_all)/ initial_price_all)*100

roi_all_companies.sort_values(ascending = False).head(10)


# Create a Mutual Fund Plan Based on High ROI and Low Risk

# For that we will have to use a combination of ROI and volatility with standard deviations metrics. 

# In[21]:


#Creating thresholds that select such companies.
roi_threshold = roi_all_companies.median()

volatility_threshold = volatility_all_companies.median()

selected_companies = roi_all_companies[(roi_all_companies> roi_threshold) & (volatility_all_companies < volatility_threshold)]

selected_companies.sort_values(ascending= False)


# To balance the investment between these companies, we can use an inverse volatility ratio for allocation. Companies with lower volatility will get a higher weight. Let’s calculate the weight for each company:

# In[23]:


selected_volatility = volatility_all_companies[selected_companies.index]

inverse_volatility = 1/ selected_volatility

investment_ratios = inverse_volatility / inverse_volatility.sum()

investment_ratios.sort_values(ascending = False)


# Analyze our Mutual Fund Plan

# In[24]:


top_growth_companies = avg_growth_all_companies.sort_values(ascending =False).head(10)

risk_growth_rate_companies = volatility_all_companies[top_growth_companies.index]

risk_mutual_fund_companies = volatility_all_companies [selected_companies.index]

fig = go.Figure()

fig.add_trace(go.Bar(
y=risk_mutual_fund_companies.index,
x= risk_mutual_fund_companies, 
orientation='h', #Horizontal Bar
name = 'Mutual Fund Companies',
marker = dict(color= 'blue')
))

fig.add_trace(go.Bar(
y= risk_growth_rate_companies.index,
x=risk_growth_rate_companies,
orientation='h',
name= 'Growth Rate Companies',
marker = dict(color= 'green'),
opacity=0.7))

fig.update_layout(
title = 'Risk Comparison: Mutual Fund vs Growth Rate Companies',
xaxis_title = 'Volatility (Standard Deviation)',
yaxis_title = 'Companies',
barmode = 'overlay',
legend = dict(title= 'Company Type'),
template = 'plotly_white')

fig.show()


# Comparing the ROI of both the groups

# In[25]:


expected_roi_mutual_fund = roi_all_companies[selected_companies.index]

expected_roi_growth_companies= roi_all_companies[top_growth_companies.index]

fig =go.Figure()

fig.add_trace(go.Bar(
y = expected_roi_mutual_fund.index,
x = expected_roi_mutual_fund, 
orientation='h',
name='Mutual Fund Companies',
marker= dict(color= 'blue')
))

fig.add_trace(go.Bar(
y = expected_roi_growth_companies.index,
x = expected_roi_growth_companies, 
orientation='h',
name='Growth Rate Companies',
marker= dict(color= 'green'),
    opacity = 0.7
))

fig.update_layout(
title = 'Expected ROI Comparison: Mutual Fund vs Growth Rate Companies',
xaxis_title = 'Expected ROI(%)',
yaxis_title = 'Companies',
barmode = 'overlay',
legend = dict(title = 'Company Type'),
template = 'plotly_white')

fig.show()


# The comparison between the risk (volatility) and expected ROI for mutual fund companies (in blue) and growth rate companies (in green) shows a clear trade-off. Mutual fund companies offer lower volatility, meaning they are less risky, but also provide lower expected returns. In contrast, growth rate companies demonstrate higher volatility, indicating more risk, but they offer much higher potential returns, especially companies like Bajaj Auto and Bajaj Finserv. This highlights a common investment dilemma: lower risk comes with a lower reward, while higher risk could yield higher returns.
# 
# For long-term investments, the goal is typically to find companies that offer a balance of stable returns and manageable risk. The companies in our mutual fund exhibit low volatility, meaning they are less risky, and their moderate returns make them solid choices for long-term, stable growth. They are well-suited for conservative investors who want steady returns without significant fluctuations in value.

# Calculating Expected Returns
# 

# Assumptions:
# 
# Assume the person is investing 5000 rupees every month.
# Use the expected ROI from the mutual fund companies to simulate the growth over time.
# Compute the compounded value of the investments for each period (1y, 3y, 5y, and 10y).
# Visualize the accumulated value over these periods.

# In[26]:


import numpy as np

monthly_investment = 5000
years = [1,3,5,10] #Investment periods in years
n = 12 #number of times compounded

avg_roi = expected_roi_mutual_fund.mean() /100 #Converting the avg_roi to decimal

def future_value(P, r,n,t):
    return P*(((1+r/n)**(n*t)-1)) *(1+r/n)

future_values = [future_value(monthly_investment, avg_roi, n,t) for t in years]

fig = go.Figure()

fig.add_trace(go.Scatter(
x= [str(year) + 'year' for year in years],
y = future_values,
mode = 'lines+markers',
line = dict(color = 'blue'),
marker = dict(size = 8),
name = 'Future Value'))

fig.update_layout(
title = 'Expected Value of Investments of Rs. 5000 Per month(Mutual Funds)',
xaxis_title = 'Investment Period',
yaxis_title = "Future Value(INR)",
xaxis = dict(showgrid= True, gridcolor = 'lightgrey'),
yaxis = dict(showgrid= True, gridcolor = 'lightgrey'),
template = 'plotly_white',
hovermode ='x'
)

fig.show()

