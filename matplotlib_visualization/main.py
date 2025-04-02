import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("QueryResults.csv", names=['DATE', 'TAG', 'POSTS'], header=0)

# Display the first and last 5 rows
print("First 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

# Get the number of rows and columns
num_rows, num_cols = df.shape
print(f"\nNumber of rows: {num_rows}, Number of columns: {num_cols}")

# Count the number of entries in each column
print("\nNumber of entries per column:")
print(df.count())

# Group by TAG and sum the POSTS column
total_posts_per_language = df.groupby('TAG')['POSTS'].sum().reset_index()
total_posts_per_language = total_posts_per_language.sort_values('POSTS', ascending=False)
print(total_posts_per_language)

# Get the programming language with the highest total posts
# iloc(does not care index) vs loc(care the index)
most_popular_language = total_posts_per_language.iloc[0]
print(f"Most popular language: {most_popular_language['TAG']} with {most_popular_language['POSTS']} posts")

# Counting Unique Months with Posts for Each Language
df['DATE'] = pd.to_datetime(df['DATE'])  # Ensure DATE column is in datetime format
df['YearMonth'] = df['DATE'].dt.to_period('M')  # Extract Year-Month
# .nunique() counts each unique ones and reset_index assigns index starting from 0
months_per_language = df.groupby('TAG')['YearMonth'].nunique().reset_index()
months_per_language.columns = ['TAG', 'Months_With_Posts']
print(months_per_language.sort_values(by='Months_With_Posts', ascending=False))


reshaped_df = df.pivot(index='DATE', columns='TAG', values='POSTS')
print(reshaped_df)

print(reshaped_df.head())
print(reshaped_df.tail())

print(reshaped_df.columns)
print(reshaped_df.count())
print(reshaped_df.sum())

# replace nan values with 0
reshaped_df = reshaped_df.fillna(0)

print(f"final {reshaped_df}")

# ---- VISUALIZATION ----
# The window defines how many observations are averaged
roll_df = reshaped_df.rolling(window=6).mean()

plt.figure(figsize=(16,10))  # Set figure size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

# Plot the rolling average instead of raw data
for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column], 
             linewidth=3, label=roll_df[column].name)

plt.legend(fontsize=16)
plt.show()
