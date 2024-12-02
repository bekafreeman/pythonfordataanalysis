# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:55:00 2024

@author: bekaf
"""

import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt 
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from textblob import TextBlob
import seaborn as sns

#Reading the CSV file
df = pd.read_csv('chatgpt1.csv')
df.drop("Username",axis=1,inplace=True)

#Creating a function to detect languages
#For an individual column
x = df['Text'][0]
lang = detect(x)

#For the whole table
def det(x):
    try:
        lang = detect(x)
    except:
        lang = 'Other'
    return lang

df['Lang'] = df['Text'].apply(det)
df = df.loc[df['Lang'] == 'en']
df = df.reset_index(drop=True)

#Cleaning some text
df['Text'] = df['Text'].str.replace('https', '')
df['Text'] = df['Text'].str.replace('http', '')
df['Text'] = df['Text'].str.replace('t.co', '')
df['Text'] = df['Text'].str.replace('amp', '')
df['Text'] = df['Text'].str.replace('ChatGPT', '')
df['Text'] = df['Text'].str.replace('Chatgpt', '')


#Developing a sentiment function
def get_sentiment(text):
    sentiment = TextBlob(text).sentiment.polarity
    
    if sentiment > 0:
        return 'positive'
    elif sentiment < 0:
        return 'negative'
    else:
        return 'neutral'
    
df['Sentiment'] = df['Text'].apply(get_sentiment)

#Genrating a WordCloud

comment_words = ""
stopwords = set(STOPWORDS)

# Generate a WordCloud
for val in df.Text:
    if pd.notnull(val): 
        val = str(val)  
        tokens = val.split() 
        comment_words += " ".join(tokens) + " "  

wordcloud = WordCloud(width=900, height=500, background_color='black', stopwords=set(STOPWORDS), min_font_size=10).generate(comment_words)

plt.figure(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout()
plt.show()

sns.set_style('whitegrid')
plt.figure(figsize=(10,5))

sns.countplot(x='Sentiment', data=df)
plt.xlabel('Sentiment')
plt.ylabel('Count of Sentiment')
plt.title('Sentiment Distribution ')
plt.show()
