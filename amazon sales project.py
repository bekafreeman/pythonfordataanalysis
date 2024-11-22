# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:54:24 2024

@author: bekaf

Questions and answers
- How many sales have they made with amounts more than 1000? - high_amount_data
- How many sales have they made that belong to the category 'Tops' and have a Quantity of 3? - filtered_data
- The total sales by category? - category_totals
- The Average amount by category and Status? - status_average
- Total sales by Fulfilment and Shipment type? - total_sales_shipandfulfil
"""

import pandas as pd

#Load sales data from an Excel file into Pandas DataFrame

sales_data = pd.read_excel('C:/Users/bekaf/Documents/sales_data.xlsx')

# =============================================================================
# Exploring the data
# =============================================================================

#Get summary of sales data & check data types
sales_data.info()

sales_data.describe()

#Looking at column names
print(sales_data.columns)

#Looking at the first few rows of data
print(sales_data.head())

#Another way to check data types
print(sales_data.dtypes)

# =============================================================================
# Cleaning the data
# =============================================================================

#Check for missing values in sales data .sum for total null/nan values in each row
print(sales_data.isnull().sum())

#Drop any rows that have any missing/nan data
sales_data_dropped = sales_data.dropna()

#Drop rows with no/nan value in the amount column
sales_data_cleaned = sales_data.dropna(subset = ['Amount'])

#Check for missing values in sales data cleaned .sum for total null/nan values in each row
print(sales_data_cleaned.isnull().sum())

# =============================================================================
# Slicing and Filtering Data
# =============================================================================

#Select a subset of our data based on the category column
catagory_data = sales_data[sales_data['Category'] == 'Top']
print(catagory_data)

#Select a subset of our data where the amount > 1000
high_amount_data = sales_data[sales_data['Amount'] > 1000]
print(high_amount_data)

#Select a subset of data based on multiple conditions
filtered_data = sales_data[(sales_data['Category'] == 'Top') & (sales_data['Qty'] == 3)]

# =============================================================================
# Aggregating Data
# =============================================================================

#Total sales by category
catagory_totals = sales_data.groupby('Category')['Amount'].sum()
#Total sales by category when the category is NOT the index
catagory_totals = sales_data.groupby('Category', as_index=False)['Amount'].sum()
#Total sales by category sorted from largest - smallest
catagory_totals = catagory_totals.sort_values('Amount', ascending=False)

# Calculate the average amount by category and fulfilment
fulfilment_averages = sales_data.groupby(['Category', 'Fulfilment'], as_index=False)['Amount'].mean()
#The average amount by category and fulfilment sorted from largest - smallest
fulfilment_averages = fulfilment_averages.sort_values('Amount', ascending=False)

#Calculate the average by Category and status & sorted largest - smallest
status_average = sales_data.groupby(['Category', 'Status'], as_index=False)['Amount'].mean()
status_average = status_average.sort_values('Amount', ascending=False)

#Calculate total sales by shipment and fulfilment
total_sales_shipandfulfil = sales_data.groupby(['Courier Status', 'Fulfilment'], as_index=False)['Amount'].sum()
total_sales_shipandfulfil = total_sales_shipandfulfil.sort_values('Amount', ascending=False)

#Renaming Courier Status column to Shipment
total_sales_shipandfulfil.rename(columns={'Courier Status': 'Shipment'}, inplace=True)

# =============================================================================
# Exporting the Data
# =============================================================================

status_average.to_excel('average_sales_by_category_and_status.xlsx', index=False)
total_sales_shipandfulfil.to_excel('total_sales_by_ship_and_fulfil.xlsx', index=False)
