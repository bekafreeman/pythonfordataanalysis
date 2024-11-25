# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 10:03:23 2024

@author: bekaf
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Set the working directory
os.chdir('C:/Users/bekaf/Documents/Python for Data Analysis/Source (Input) Data for the course/Ecommerce Orders Project')

#Check current working directory
print(os.getcwd())

# =============================================================================
# Loading Files
# =============================================================================

#Load the order data
orders_data = pd.read_excel('orders.xlsx')

#Load payment data. If .csv file you would use pd.read_csv('filename.csv')
payments_data = pd.read_excel('order_payment.xlsx')

#Load customers data
customers_data = pd.read_excel('customers.xlsx')

# =============================================================================
# Describing the data
# =============================================================================

orders_data.info()
payments_data.info()
customers_data.info()

#Handelling missing data

#Check for missing data in the orders data
orders_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

#Replacing the missing values in orders data with a default value
orders_data2 = orders_data.fillna('N/A')
#Check if null values in oreders_data2
orders_data2.isnull().sum()

#Drop the rows with missing values in payment data
payments_data = payments_data.dropna()
#Check if null values in payments_data
payments_data.isnull().sum()

# =============================================================================
# Removing duplicate data
# =============================================================================

#Check for duplicates in orders data
orders_data.duplicated().sum()

#Remove duplicates
orders_data = orders_data.drop_duplicates()

#Check for duplicates in payment data
payments_data.duplicated().sum()

#Remove duplicates
payments_data = payments_data.drop_duplicates()

# =============================================================================
# FLitering the data
# =============================================================================

#Select a subset of orders data based on order status
invoiced_orders_data = orders_data[orders_data['order_status'] == 'invoiced']
#Reset the index
invoiced_orders_data = invoiced_orders_data.reset_index(drop=True)

#Select a subset of payments data where payments type = credict card  + payment value > 1000
credit_card_payments_data = payments_data[
    (payments_data['payment_type'] == 'credit_card') & 
    (payments_data['payment_value'] > 1000)
    ]

#Select a subset of customers based on customer state = SP
customer_data_state = customers_data[customers_data['customer_state'] == 'SP']

# =============================================================================
# Merge and Join DataFrames
# =============================================================================


#Merge orders data with paymenys data on order_id columns
merged_data = pd.merge(orders_data, payments_data, on='order_id')

#Join merged data with cutomer data on cutomer_id column
joined_data = pd.merge(merged_data, customers_data, on='customer_id')

# =============================================================================
# Data Visualisation
# =============================================================================

#Create a field called month_year from order_purchase_timstamp
joined_data['year_month'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['year_week'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')

grouped_data = joined_data.groupby('year_month')['payment_value'].sum()
grouped_data = grouped_data.reset_index()

#COnvert year_month from period data type to string
grouped_data['year_month'] = grouped_data['year_month'].astype(str)

#Creating a plot

plt.plot(grouped_data['year_month'], grouped_data['payment_value'], color='red', marker='o')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Year and Month')
plt.ylabel('Payment Value')
plt.title('Payment Value by Month and Year')
plt.xticks(rotation = 90, fontsize=8)
plt.yticks(fontsize=8)
plt.show()

#Scatter plot

#Create DataFrame
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value': 'sum', 'payment_installments': 'sum'})

plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Installments by Customer')
plt.show()

#Using seaborn to create a scatter plot

sns.set_theme(style='darkgrid') #other style options: whitegrid, darkgrid, dark, white
sns.scatterplot(data=scatter_df, x='payment_value', y='payment_installments')
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Installments by Customer')
plt.show()

#Creating a bar chart
bar_chart_df = joined_data.groupby(['payment_type', 'year_month'])['payment_value'].sum()
bar_chart_df = bar_chart_df.reset_index()

pivot_data = bar_chart_df.pivot(index='year_month', columns='payment_type', values='payment_value')

pivot_data.plot(kind='bar', stacked='True')
plt.ticklabel_format(useOffset=False, style='plain', axis='y')
plt.xlabel('Month of Payment')
plt.ylabel('Payment Value')
plt.title('Payment per Payment Type by Month')
plt.show()

#Creating a box plot

payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

#Creating a boxplot per payment types
plt.boxplot([payment_values[payment_types == 'credit_card'],
             payment_values[payment_types == 'boleto'],
             payment_values[payment_types == 'voucher'],
             payment_values[payment_types == 'debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
            )
#Set labels and title
plt.xlabel('Payment Type')
plt.ylabel('Paymant Values')
plt.title('Box Plot showing Payment Value ranges by Payment Type')
plt.show()

#Creating a subplot(3 plots in one)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10,10))

#ax1 which is a box plot
ax1.boxplot([payment_values[payment_types == 'credit_card'],
             payment_values[payment_types == 'boleto'],
             payment_values[payment_types == 'voucher'],
             payment_values[payment_types == 'debit_card']],
            labels = ['Credit Card', 'Boleto', 'Voucher', 'Debit Card']
            )
#Set labels and title
ax1.set_xlabel('Payment Type')
ax1.set_ylabel('Paymant Values')
ax1.set_title('Box Plot showing Payment Value ranges by Payment Type')

#ax2 is stacked bar cahrt

pivot_data.plot(kind='bar', stacked='True', ax=ax2)
ax2.ticklabel_format(useOffset=False, style='plain', axis='y')
#Set labels and titles
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment Value')
ax2.set_title('Payment per Payment Type by Month')

#ax3 is a scatter plot
plt.scatter(scatter_df['payment_value'], scatter_df['payment_installments'])
#Set labels and titles
ax3.set_xlabel('Payment Value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Value vs Installments by Customer')

fig.tight_layout() # Sorts out overlapping labels

plt.savefig('my_plot.png') #TO save the image

plt.show()