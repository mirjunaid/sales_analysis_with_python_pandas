# Importing the required libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

# Preparing the data set for analysis
path = "C:/Users/SW/Downloads/datasets/Sales_Data"
files = [file for file in os.listdir(path) if not file.startswith('.')]  # Ignore the hidden files

all_months_data = pd.DataFrame()

for file in files:
    current_data = pd.read_csv(path + "/" + file)
    all_months_data = pd.concat([all_months_data, current_data])

all_months_data.to_csv("yearly_data_2019.csv", index=False)

# Read the dataframe
data = pd.read_csv('yearly_data_2019.csv')
# print(data.head())

# CLEAN THE DATA
# Find NAN
nan_df = data[data.isna().any(axis=1)]
# print(nan_df.head())

# Drop the NaN columns
data = data.dropna(how='all')

# Change the format of the order date column to datetime format
data = data[data['Order Date'].str[0:2] != 'Or']
data['Order Date'] = pd.to_datetime(data['Order Date'])

# Make columns correct type
data['Quantity Ordered'] = pd.to_numeric(data['Quantity Ordered'])
data['Price Each'] = pd.to_numeric(data['Price Each'])

# Add a column
data['Month'] = data['Order Date'].dt.month
data['Hour'] = data['Order Date'].dt.hour

# Add a city column
def get_city(address):
    return address.split(',')[1].strip(' ')


def get_state(address):
    return address.split(',')[2].split(' ')[1]


data['City'] = data['Purchase Address'].apply(lambda x: f'{get_city(x)}  {get_state(x)}')

# Add a sales column to find money earned by selling different products
data['Sales'] = data['Quantity Ordered'].astype('int') * data['Price Each'].astype('float')
print(data.head())

# NOW LETS GET STARTED WITH THE DATA EXTRACTION PART

# Question 1:What month had the maximum sales
# plot the graph to compare sale of all the months
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
new_colors = ['violet', 'indigo', 'blue', 'green', 'yellow', 'orange', 'red', 'maroon', 'gray', 'silver', 'gold', 'brown']

plt.bar(months, data.groupby('Month').sum()['Sales'], color=new_colors, width=0.8, edgecolor='black')
plt.title('Graph for the sales done in all months of 2019', size=14)
plt.xticks(months, rotation='vertical', size=8)
plt.xlabel('Month Name', size=14)
plt.ylabel('Sales amount in millions(USD $)', size=14)
plt.show()

# Question 2: What city had the maximum sales
cities = [city for city, df in data.groupby(['City'])]
city_sales_sum = data.groupby('City').sum()['Sales']

plt.bar(cities, city_sales_sum, color=new_colors, width=0.8, edgecolor='black')
plt.title('Graph for the sales done in different cities in 2019', size=14)
plt.xticks(cities, rotation='vertical', size=8)
plt.xlabel('City Name', size=14)
plt.ylabel('Sales amount in millions(USD $)', size=14)
plt.show()

# Question 3: What time were the maximum orders made
hours = [hour for hour, df in data.groupby(['Hour'])]
hour_sale_sum = data.groupby('Hour').sum()['Sales']

plt.bar(hours, hour_sale_sum, color=new_colors, width=0.8, edgecolor='black')
plt.title('Graph for the overall sales done in different hours in 2019', size=14)
plt.xticks(hours, rotation='vertical', size=8)
plt.xlabel('Clock Hours', size=14)
plt.ylabel('Sales amount in millions(USD $)', size=14)
plt.show()

# Question 4: What products are most often sold together?
df = data[data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df2 = df[['Order ID', 'Grouped']].drop_duplicates()
count = Counter()

for row in df2['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

for key, value in count.most_common(10):
    print(key, value)

plt.bar(key, value, color=new_colors, width=0.8, edgecolor='black')
plt.title('Graph for the overall sales done in different hours in 2019', size=14)
plt.xticks(key, rotation='vertical', size=8)
plt.xlabel('Product Combinations', size=14)
plt.ylabel('Sales amount in millions(USD $)', size=14)
plt.show()
