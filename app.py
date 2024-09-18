

# Make sure to install your dependency
# python -m pip install Flask
# BCG/app.py

# Load important libraries
from flask import Flask
import pandas as pd
from pathlib import Path
DATA_PATH = Path('C:\\Users\good\\gitmedia\\ProjectForage\\forage_bcg')

# from google.colab import drive
# drive.mount('/content/gdrive')

# DATA_PATH = Path('gdrive/My Drive/fbcg/')

df = pd.read_csv(DATA_PATH / 'apple22.csv')

# Load important libraries

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# Year-over-Year Net Income and revenue growth
df['Revenue Growth (%)'] = df.groupby(['Company'])['Total Revenue'].pct_change() * 100
df['Net Income Growth (%)'] = df.groupby(['Company'])['Net Income'].pct_change() * 100

# Summarize financial metrics by Company
summary1 = df.groupby('Company').agg({
    'Net Income': ['sum', 'mean'],
    'Total Revenue': ['sum', 'mean'],
    'Total Assets': ['sum', 'mean'],
    'Cash Flow': ['sum', 'mean'],
})


# Summarize financial metrics by Year
summary2 = df.groupby('Year').agg({
    'Net Income': ['sum', 'mean'],
    'Total Liabilities': ['sum', 'mean'],
    'Cash Flow': ['sum', 'mean'],
})

# Financial metrics grouped by both Company and Year
summary3 = df.groupby(['Company', 'Year']).agg({
    'Net Income': ['sum', 'mean'],
    'Total Revenue': ['sum', 'mean'],
    'Total Assets': ['sum', 'mean'],
})



# Rolling window (e.g., 3-year moving average of Net Income)
summary4 = df.set_index('Year').groupby('Company')['Net Income'].rolling(window=3).mean()

# Rank companies by Net Income per Year
df['Net Income Rank'] = df.groupby('Year')['Net Income'].rank(ascending=False)
summary5= df.groupby('Company')['Total Revenue'].cumsum()
# summary5

summary6 = df.pivot_table(index='Year', columns='Company', values=['Net Income', 'Total Revenue'], aggfunc='sum')
# summary6

# CAGR (Compound Annual Growth Rate) for Total Revenue
no_of_years = 3

cagr = (df.groupby('Company')['Total Revenue'].last() / df.groupby('Company')['Total Revenue'].first())**(1/no_of_years) - 1

df['Net Income Rank'] = df.groupby('Year')['Net Income'].rank(ascending=False)

def financial_analysis(df, company, year):
    # Filter data for the specified company and year
    company_data = df[(df['Company'] == company) & (df['Year'] == year)]
    company_data_prev = df[(df['Company'] == company) & (df['Year'] == year - 1)]

    # Basic checks
    if company_data.empty:
        return f"No data available for {company} in year {year}."

    # Total Revenue
    total_revenue = company_data['Total Revenue'].sum()

    # Net Income Change (YoY % change)
    if not company_data_prev.empty:
        net_income_current = company_data['Net Income'].sum()
        net_income_previous = company_data_prev['Net Income'].sum()
        net_income_change = ((net_income_current - net_income_previous) / net_income_previous) * 100 if net_income_previous != 0 else 'N/A'
    else:
        net_income_change = 'N/A'  # No previous year data

    # Gross Margin %
    net_income = company_data['Net Income'].sum()
    gross_margin = (net_income / total_revenue) * 100 if total_revenue != 0 else 'N/A'

    # ROE (Return on Equity)
    total_assets = company_data['Total Assets'].sum()
    total_liabilities = company_data['Total Liabilities'].sum()
    total_equity = total_assets - total_liabilities
    roe = (net_income / total_equity) * 100 if total_equity != 0 else 'N/A'

    # Debt-to-Equity Ratio
    debt_to_equity = (total_liabilities / total_equity) if total_equity != 0 else 'N/A'

    # Revenue Mix Change (YoY change in revenue)
    if not company_data_prev.empty:
        revenue_previous = company_data_prev['Total Revenue'].sum()
        revenue_change = ((total_revenue - revenue_previous) / revenue_previous) * 100 if revenue_previous != 0 else 'N/A'
    else:
        revenue_change = 'N/A'

    # Highest Ranked Company (Based on Net Income Rank)
    highest_ranked_company = df[df['Net Income Rank'] == df['Net Income Rank'].min()]['Company'].values[0]

    # Prepare the result dictionary
    result = {
        "Company": company,
        "Year": year,
        "Total Revenue": total_revenue,
        "Net Income Change (YoY %)": net_income_change,
        "Gross Margin (%)": gross_margin,
        "Return on Equity (ROE %)": roe,
        "Debt-to-Equity Ratio": debt_to_equity,
        "Revenue Mix Change (YoY %)": revenue_change,
        "Highest Ranked Company": highest_ranked_company
    }

    return result

import random

def simple_chatbot2(user_query):

    answers1 = financial_analysis(df, "Microsoft", 2003)    # answers1
    answers2 = financial_analysis(df, "Apple", 2003) # answers2
    answers3 = financial_analysis(df, "Tesla", 2003)

    responses = {"What is the total revenue for the year 2003?": "The total revenue for Apple is {}".format(answers2["Total Revenue"]) ,
"How has net income changed over the year?": "The net come changed by a percentage of {}".format(answers1["Total Revenue"]),
"What is the company's gross margin percentage Return-on-Equity(ROE)?": "The ROE for Microsoft is {}".format(answers1["Return on Equity (ROE %)"]),
"What is the company's Debt to Equity ratio?": "For Microsoft, it is {}".format(answers3["Debt-to-Equity Ratio"]),
"How has the company's revenue mix changed overtime": "The revenue mix for Apple changed by {}".format(answers2["Revenue Mix Change (YoY %)"]),
"Which company is the best performing company": answers1["Highest Ranked Company"]
}
    if user_query in responses:
    # random.choice()
        return responses[user_query]


# ["The total revenue for Apple is {}".format(answers2["Total Revenue"]),
# "The total revenue for Microsoft is {}".format(answers1["Total Revenue"]), "The total revenue for Tesla is {}".format(answers3["Net Income Change (YoY %)"])]

# Define a decorator function
# for the flask view
@app.route('/')
# ‘/’ URL is bound with prompt_view function.
def prompt_view():
    print("Make your query in the box below: ")
    input_prompt = input()

    output_answer = simple_chatbot2(user_query=input_prompt)
    return output_answer

# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)

# Run the app.py flask program in a terminal
# python app.py
# Then open a browser at https:localhost/5000
# Enter the prompt:
# 1. Which company is the best performing company: Apple
# 2. What is the total revenue for the year 2003?: The total revenue for Apple is 12.4
# 3. What is the company's gross margin percentage Return-on-Equity(ROE)?: The ROE for Microsoft is 35.088714643856406