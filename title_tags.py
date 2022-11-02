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
import spacy
from collections import Counter

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

# Next we are going to analyze the most improtant terms in the title. Before we do this, we need to pull all the text together.    

df['title'] = df['title'].astype(str)
text = " ".join([x for x in df["title"].tolist()if len(x) > 0])

#

nlp = spacy.load('en')
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
