# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 13:49:03 2024

@author: bekaf
"""

import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

#Read the Excel files
pizza_sales_df = pd.read_excel('pizza_sales.xlsx')
pizza_size_df = pd.read_csv('pizza_size.csv')
pizza_category_df = pd.read_csv('pizza_category.csv')

#Viewing top + bottom rows in a DataFrame
pizza_sales_df.head()
pizza_sales_df.head(10)

pizza_sales_df.tail()
pizza_sales_df.tail(10)

#Describing the data
pizza_sales_df.describe()
pizza_description = pizza_sales_df.describe()

#Check no null counts per column
pizza_sales_df.info()

#Count the number of nulls
null_count = pizza_sales_df.isnull().sum()

#Check from duplicated rows
duplicated_rows = pizza_sales_df.duplicated().sum()
print(duplicated_rows)

#To select single/multiple column(s)
quantity_column = pizza_sales_df['quantity']
selected_column = pizza_sales_df[['order_id', 'quantity', 'unit_price']]

#Get the row with index label 3
row = pizza_sales_df.loc[3]

#Get two rows with index labels 3 and 5
rows = pizza_sales_df.loc[[3, 5]]

#Get rows between index labels 3 - 5
subset = pizza_sales_df.loc[3:5]

#Get rows between index labels 3 - 5 and specific columns
subset = pizza_sales_df.loc[3:5, ['quantity', 'unit_price']]

#Set an index as a column in a data frame
pizza_sales_df.set_index('order_details_id', inplace=True)

#Resetting an index
pizza_sales_df.reset_index(inplace=True)

#Truncate dataframe before index 3
truncate_before = pizza_sales_df.truncate(before=3)

#Truncate dataframe after index 5
truncate_after = pizza_sales_df.truncate(after=5)

#Truncate columns
quantity_series = pizza_sales_df['quantity']
 
#Truncate series before index 3
truncate_series_before = quantity_series.truncate(before=3)

#Truncate series after index 5
truncate_series_after = pizza_sales_df.truncate(after=5)

#Basic filtering
filtered_rows = pizza_sales_df[pizza_sales_df['unit_price'] > 20]

#Filtering on date
pizza_sales_df['order_date'] = pizza_sales_df['order_date'].dt.date
date_target = datetime.strptime('2015-12-15', '%Y-%m-%d').date()
filtered_rows_by_date = pizza_sales_df[pizza_sales_df['order_date'] > date_target]

#Filtering on multiple conditions
#Using and condition (&)
bbq_chicken_rows = pizza_sales_df[(pizza_sales_df['unit_price'] > 10)
                                  & (pizza_sales_df['pizza_name'] == 'The Barbecue Chicken Pizza')]

#Using the or condition (|)
bbq_chicken_rows_or = pizza_sales_df[(pizza_sales_df['unit_price'] > 20)
                                  | (pizza_sales_df['pizza_name'] == 'The Barbecue Chicken Pizza')]

#Filter a specific range
high_sales = pizza_sales_df[(pizza_sales_df['unit_price'] > 15) 
                            & (pizza_sales_df['unit_price'] <= 20)]

#Dropping null values
pizza_sales_null_values_dropped = pizza_sales_df.dropna()
null_count = pizza_sales_null_values_dropped.isnull().sum()

#Replace null with a value
date_na_fill = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
pizza_sales_null_replaced = pizza_sales_df.fillna(date_na_fill)

#Deleting specific rows and columns in a dataframe
filter_rows_2 = pizza_sales_df.drop(2, axis=0)

#Deleting multiple rows (5, 7 and 9)
filter_rows_5_7_9 = pizza_sales_df.drop([5,7,9], axis=0)

#Delete a column by column name
filtering_unit_price = pizza_sales_df.drop('unit_price', axis=1)

#Delete multiple columns
filtering_unit_price_and_order_id = pizza_sales_df.drop(['unit_price', 'order_id'], axis=1)

#Sorting a dataframe in Pandas

#Sorting in ascending order
sorted_df = pizza_sales_df.sort_values('total_price')

#Sorting in descending order
sorted_df = pizza_sales_df.sort_values('total_price', ascending=False)

#Sort by multiple columns
sorted_df = pizza_sales_df.sort_values(['pizza_category_id', 'total_price'], ascending=[True, False])

#Group by pizza_size_id and get count of sales (row count)
grouped_df_pizza_size = pizza_sales_df.groupby(['pizza_size_id']).count()

#Group by pizza_size_id and get the sum
grouped_df_pizza_size_sum = pizza_sales_df.groupby(['pizza_size_id'])['total_price'].sum()

#Gorup by pizza_size_id and sum of total_price and quantity
grouped_df_pizza_size_quantity = pizza_sales_df.groupby(['pizza_size_id'])[['total_price', 'quantity']].sum()

"""
Looking at different aggregation functions
count(): counts the number of non-null/non-NA values in each group
sum() : sums the values in each group
mean() : calculates the average of the values in each group
std() : computes the standard deviation in each group
var() : computes the standard variance in each group
min() : find the minimum value in each group
max() : finds the maximum value in each group
prod() : computes the product of values in each group
first(), last() : gets the first and last values in each group
size() : returns the size of each group, including NA/NaN values
nunique() : counts the number of unique values in each group
"""

#Using agg to perform different aggregations on different columns
aggregated_data = pizza_sales_df.groupby(['pizza_size_id']).agg({'quantity':'sum', 'total_price':'mean'})

#Murging 2 dataframes (pizza_sales_df and pizza_size_df)
merged_df = pd.merge(pizza_sales_df, pizza_size_df, on='pizza_size_id')
#Add category information
merged_df = pd.merge(merged_df, pizza_category_df, on='pizza_category_id')

#Concatanate two dataframes - appending rows to a dataframe - concatenate vertically
another_pizza_sales_df = pd.read_excel('another_pizza_sales.xlsx')
concatenate_vertically = pd.concat([pizza_sales_df, another_pizza_sales_df])
concatenate_vertically = concatenate_vertically.reset_index()

#Concatenate 2 dataframes - appending columns to a dataframe - horizontally 
pizza_sales_voucher_df = pd.read_excel('pizza_sales_voucher.xlsx')
concatenate_horizontally = pd.concat([pizza_sales_df, pizza_sales_voucher_df], axis = 1)

#Converting text to lowercase
lower_text = pizza_sales_df['pizza_ingredients'].str.lower()
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.lower()
#Convert text to UPPERCASE
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.upper()
#Convert text to Titlecase
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.title()

#Replaceing text values
replaced_text = pizza_sales_df['pizza_ingredients'].str.replace('Feta Cheese', 'Mozzarella')
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.replace('Feta Cheese', 'Mozzarella')

#Removing extra whitespaces
pizza_sales_df['pizza_name'] = pizza_sales_df['pizza_name'].str.strip()

#Generating a boxplot

sns.boxplot(x='category', y='total_price', data=merged_df)
plt.xlabel('Pizza Category')
plt.ylabel('Total Sales')
plt.title('Boxplot showing distribution of sales by category')
plt.show()
