import streamlit as st
import requests
import urllib
import pandas as pd
import numpy as np
import plotly.express as px
from requests_html import HTML
from requests_html import HTMLSession
import requests
import random
user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
url = 'https://httpbin.org/headers'
for i in range(1,4):
#Pick a random user agent
    user_agent = random.choice(user_agent_list)
#Set the headers 
    headers = {'User-Agent': user_agent}
#Make the request
    response = requests.get(url,headers=headers)

st.title('Title Tag Optimization')

st.subheader('Add Your Data')

query = st.text_input("Put Your Target Keyword Here", value="Add Your Keyword")


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response 
    except requests.exceptions.RequestException as e:
        print(e)
       
def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)
    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def get_results(query):
    
    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.com/search?q=" + query)
    
    return response

def parse_results(response):
    
    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".IsZvec"
    
    results = response.html.find(css_identifier_result)

    output = []
    
    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href']
        }
        
        output.append(item)
        
    return output


def google_search(query):
    response = get_results(query)
    return parse_results(response)

if query is not None:
    results = google_search(query)
    df = pd.DataFrame(results)

if st.checkbox('Show SERP Data'):
    st.subheader('Top Ten Results')
    st.write(df)

df['title'] = df['title'].astype(str)
text = " ".join([x for x in df["title"].tolist()if len(x) > 0])

import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
set(stopwords.words('english'))

# set of stop words
stop_words = set(stopwords.words('english')) 

# tokens of words  


word_tokens = word_tokenize(text) 
filtered_sentence = []
    
  
for w in word_tokens: 
    if w not in stop_words: 
        filtered_sentence.append(w) 


import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

doc = nlp(text)
# all tokens that arent stop words or punctuations
words = [token.text
         for token in doc
         if not token.is_stop and not token.is_punct]

# noun tokens that arent stop words or punctuations
nouns = [token.text
         for token in doc
         if (not token.is_stop and
             not token.is_punct and
             token.pos_ == "NOUN")]

# five most common tokens
word_freq = Counter(words)
common_words = word_freq.most_common(10)

# five most common noun tokens
noun_freq = Counter(nouns)
common_nouns = noun_freq.most_common(10)


df_common_words = pd.DataFrame(common_words, columns = ['Word', 'Frequencey'])

st.subheader('Most Common Words In The SERPs')
st.table(df_common_words)
fig = px.bar(df_common_words, x='Word', y='Frequencey', )
fig.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig)


st.subheader("Title Tag Optimization")
title_text = st.text_input("Add Your Current Title Tag Here")


common_words, frequencey = map(list, zip(*common_words))

def title_optimization():
  if len(title_text) >= 60:
   return "Your title is too long."
  else:
   return "Your title meets length requirements."

def has_terms(): 
  if any(x in title_text for x in common_words):
    return "Your title tag contains important terms."
  else:
    return "Your title tag is missing important terms."

def missing_text(): 
    missing = [i for i in common_words if i not in title_text] 
    return missing

title_length = title_optimization()
title_characters = len(title_text)
title_characters = str(title_characters)
title_keywords = has_terms()
title_missing_keywords = missing_text()


st.subheader('Here are your reuslts')
st.write(title_length)

st.write('Your title has' + ' ' + title_characters + ' ' +  'characters')

st.write(title_keywords)

st.write('Add these terms to your title tag.')

st.table(title_missing_keywords)


