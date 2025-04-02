import pandas as pd
import requests 
from bs4 import BeautifulSoup

# Set float display format (optional, but place it early)
pd.options.display.float_format = '{:,.2f}'.format

# Load the dataset
df = pd.read_csv("salaries_by_college_major.csv")

print(df)

# Remove any NaN rows
clean_df = df.dropna()

# View the first few rows
print(clean_df.tail())

# Check the number of rows and columns
print(clean_df.shape)

# View column names
print(clean_df.columns)

# Check for missing values
print(clean_df.isna().sum())

# View the last few rows to check for any extra data
print(clean_df.tail())

# This creates a new DataFrame without rows that contain NaN values.
clean_df = df.dropna()

# This displays only the values from that column.
print(clean_df['Starting Median Salary'])

print(clean_df['Starting Median Salary'].max())
max_index_median_salary= clean_df['Starting Median Salary'].idxmax()
print(max_index_median_salary)

# major name at that index:
print(clean_df['Undergraduate Major'].loc[43])
print(clean_df['Undergraduate Major'][43])
print(clean_df.loc[43])

# Mid-career lowest
max_index_mid_career = clean_df['Mid-Career Median Salary'].idxmax()
print(clean_df.loc[max_index_mid_career])

# mid-career salary lowest
min_mid_career = clean_df['Mid-Career Median Salary'].idxmin()
print(clean_df.loc[min_mid_career])

# Calculate and add the 'Spread' column (Difference between 90th and 10th percentile salaries)
spread_col = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
clean_df.insert(1, 'Spread', spread_col)
print(clean_df.head())

# Sort by the least risky major (smallest Spread)
low_risk = clean_df.sort_values('Spread')
print(low_risk[['Undergraduate Major', 'Spread']].head())

# Sort by the most lucrative major (highest 90th percentile salary)
high_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
print(high_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head())

# Sort by the most volatile major (largest Spread)
high_risk = clean_df.sort_values('Spread', ascending=False)
print(high_risk[['Undergraduate Major', 'Spread']].head())

# Counting Majors in Each Group
group_counts = clean_df.groupby('Group').count()
print(group_counts)

# Finding the Average Salary by Group
group_means = clean_df.groupby('Group')[['Starting Median Salary', 'Mid-Career Median Salary']].mean()
print(group_means)


# ---- Web Scraping for Updated Salary Data ----

URL = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors"

response = requests.get(URL)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "lxml")

salary_table = soup.find('table')  
rows = salary_table.find_all('tr')[1:]

salary_data = []
for row in rows:
    columns = row.find_all('td')
    major = columns[1].text.replace("Major:", "").strip()
    # Extract only integer numbers from salary values
    starting_salary = int(''.join(filter(str.isdigit, columns[3].text.strip())))
    mid_career_salary = int(''.join(filter(str.isdigit, columns[4].text.strip())))
    
    salary_data.append([major, starting_salary, mid_career_salary])

# print(salary_data)

salary_df = pd.DataFrame(salary_data, columns=['Major', 'Starting Salary', 'Mid-Career Salary'])

print(salary_df)
