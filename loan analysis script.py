# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:02:54 2024

@author: bekaf
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

loan_data = pd.read_excel('loandataset.xlsx')
customer_data = pd.read_csv('customer_data.csv', sep=';')

#Display the first few rows of the dataset
print(loan_data.head())
print(customer_data.head())

#Merging 2 dataframes on 1 column
complete_data = pd.merge(loan_data, customer_data, left_on= 'customerid', right_on = 'id')

#Check for missing data
complete_data.isnull().sum()

#Remove the rows with missing data
complete_data = complete_data.dropna()
complete_data.isnull().sum()

#Check for duplicate data
complete_data.duplicated().sum()
#Dropping duplicated
complete_data = complete_data.drop_duplicates()

#Functions in Python
"""
Template of a function
def function_name(parameter1, parameter2):
    the operation that needs to be done
    return specific result
"""

def add_numbers(number1, number2):
    sum = number1 + number2
    return sum

result = add_numbers(10, 15)
print(result)

#Define a function to categorise purpose into broader categories
def catagorise_purpose(purpose):
    if purpose in ['credit_card', 'debt consolidation']:
        return 'Financial'
    elif purpose in ['educational', 'small_business']:
        return 'Educational/Business'
    else:
        return 'Other'

catagorise_purpose('credit_card')

complete_data['purpose_category'] = complete_data['purpose'].apply(catagorise_purpose)

#Creating a conditional statement function

def check_number(number):
    if number > 0:
        return 'Positive'
    elif number< 0:
        return 'Negative'
    else:
        return 'Zero'

result = check_number(0)
print(result)

#Create a new function based on a criteria
#If the dti > 20, delinq.2years > 2 and revol.util. > 60 then the borrower = high risk 

def assess_risk(row):
    if row['dti']>20 and row ['delinq.2yrs']>2 and row['revol.util']>60:
        return 'High Risk'
    else:
        return 'Low Risk'
#Adding column to dataframe to show function
complete_data['Risk'] = complete_data.apply(assess_risk, axis=1)

#Create a new function to categorise FICO scores

def catagorise_fico(fico_score):
    if fico_score >= 800 and fico_score <= 850:
        return 'Excellent'
    elif fico_score >= 740 and fico_score < 800:
        return 'Very Good'
    elif fico_score >= 670 and fico_score < 740:
        return 'Good'
    elif fico_score >= 580 and fico_score <670:
        return 'Fair'
    else:
        return 'Poor'

complete_data['fico_category'] = complete_data['fico'].apply(catagorise_fico)

#Identify customers with more than average inquiries and derogatory records with a function

def high_inc_derog(row):
    average_inq = complete_data['inq.last.6mths'].mean()
    average_derog = complete_data['pub.rec'].mean()
    if row['inq.last.6mths'] > average_inq and row['pub.rec']>average_derog:
        return 'True'
    else:
        return 'False'

complete_data['High_Inquirese_and_Public_Records'] = complete_data.apply(high_inc_derog, axis=1)

#An introduction to classes

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def greet(self):
        return f"Hello, my name is {self.name} and I am {self.age} years old"
    
    def adult(self):
        if self.age > 18:
            return "I am an adult"
        else:
            return "I am not an adult"

#Create an instance of a class
person1 = Person("Beka", 30)
person1.greet()
person1.adult()

#Creating a data analysis class to calculate summary statistics
class DataAnalysis:
    def __init__(self, df, column_name):  
        self.df = df
        self.column_name = column_name  
        
    def calculate_mean(self):
        return self.df[self.column_name].mean()  
    
    def calculate_median(self):  
        return self.df[self.column_name].median()  


analysis = DataAnalysis(complete_data, 'fico')
mean_fico = analysis.calculate_mean()
median_fico = analysis.calculate_median()

#Data visualisation

#Set the style of the visualisations
sns.set_style('darkgrid')

#Bar plot to show the distribution of loans by purpose
plt.figure(figsize=(10,6))
sns.countplot(x = 'purpose', data = complete_data, palette = 'pastel')
plt.title('Loan purpose distribution')
plt.xlabel('Purpose of loans')
plt.ylabel('Number of Loads')
plt.xticks(rotation=45)
plt.show()

#Create a scatter plot for 'dti' vs 'Income'
plt.figure(figsize=(10,6))
sns.scatterplot(x='log.annual.inc', y='dti', data=complete_data)
plt.title('Debt-To-Income Ratio vs Annual Income')
plt.show()

#Distribution of FICO scores
plt.figure(figsize=(10,6))
sns.histplot(complete_data['fico'], bins=30, kde=True)
plt.title('Distribution of FICO score')
plt.show()

#Box plot to determine risk vs interest rate
plt.figure(figsize=(10,6))
sns.boxplot(x='Risk', y='int.rate', data=complete_data)
plt.title('Interest Rate vs Risk')
plt.show()

#Subplots

#Initialize the subplot figure
fig, axs = plt.subplots(2,2,figsize=(20,20))

#1. Loan Purpose Distribution
sns.countplot(x='purpose', data=complete_data, ax=axs[0,0])
axs[0,0].set_title('Loan Purpose Distribution')
plt.setp(axs[0,0].xaxis.get_majorticklabels(), rotation=45)

#2. Debt-to-Income Ratio vs FICO Score
sns.scatterplot(x='fico', y='dti', data=complete_data, ax=axs[0,1])
axs[0,1].set_title('Debt-to-Income Ratio vs FICO Score')

#3 Distribution of FICO Score
sns.histplot(complete_data['fico'], bins=30, kde=True, ax=axs[1,0])
axs[1,0].set_title('Distribution of FICO Score')

#4 Risk Category vs Interest Rate
sns.boxplot(x='Risk', y='int.rate', data=complete_data, ax=axs[1,1])
axs[1,1].set_title('Risk Category vs Interest Rate')

#Adjust laypit for readability
plt.tight_layout()
plt.show()
