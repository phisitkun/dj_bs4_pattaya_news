#### scrape_only ####

import requests, csv
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import psycopg2
import re
import json


################################################################
# Function to create a connection to the PostgreSQL database
################################################################
#
def create_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="root",
            host="localhost",
            port="5432",
            database="pattaya_news"
        )
        return connection
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database")
        print(e)



############################## 
# Function Remove HTML Tag
##############################
#
def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


############################## 
# Function Convert to JSON
##############################
#
def convert_to_json(py_object):
    try:
        json_str = json.dumps(py_object)
        return json_str
    except Exception as e:
        # Handle the exception as needed
        print(f"Error converting to JSON: {e}")
        return None



##############################
# Get content from Link URL
##############################
#
def get_content_json(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', attrs={"class":"entry-title"}).text
    short_link = soup.find('link',{'rel':'shortlink'}).get('href')
    content = soup.find_all(["h3", "p"])
    entry_date = post.find('time', class_='entry-date').text.strip()
    
    # Convert Array to String
    content_str = ''.join(map(str, content))
    
    content_final = remove_html_tags(content_str)
    
    date_format = '%A, %d %B %Y, %H:%M'
    date_obj = datetime.strptime(entry_date, date_format)
    
    datetimestamp = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    obj_data = {
            'title': title,
            'short_link': short_link,
            'content': content_final,
            'entry_date': datetimestamp,
            }
    
    json_data = convert_to_json(obj_data)
    
    print("\n\n\njson_data => ",json_data)    
    
    # return_data = {
    #     'title' : title,
    #     'content' : content_final,
    #     'json_data' : json_data
    # }
    
    return json_data




############################################################
# Function to insert news into the PostgreSQL database
############################################################
#
def insert_news(cursor, title, content, entry_date, link):
    query = "INSERT INTO scraper_pagecontent (url, title, content, json, entry_date) VALUES (%s, %s, %s, %s) RETURNING id"
    cursor.execute(query, (cursor, title, content, entry_date, link))
    return cursor.fetchone()[0]

    
# Extract news information from the website
news_entries = {} #LIST for Insert to DATABASE

# Create a connection to the PostgreSQL database
connection = create_connection()

if connection:
    print("Database Connected!!")       
else: 
    print("Database Connect Failed!!")


###########################################
##### Start Get Info from Website URL #####
###########################################
#
url = 'https://thepattayanews.com'
response = requests.get(url)
today = date.today()
news_entries = {} # Variable for news insert to DB

class NewsEntry:
            def __init__(self, title, content, entry_date, link):
                self.title = title
                self.content = content
                self.entry_date = entry_date
                self.link = link

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    total = 0
    news_all = {}
    

    for post in posts:
        # get content by post
        total = total+1
        try:
            
            title = post.find('h3', attrs={"class":"entry-title"}).text
            # content = post.find('div',attrs={"class":"td-excerpt"}).text
            link = post.find('h3',attrs={"class":"entry-title"}).find('a').get('href')
            entry_date = post.find('time', class_='entry-date').text.strip()
            
            content = get_content_json(link)
            
            news = {
                    'title':title, 
                    'content':content['content'], 
                    'entry_date':content['json_data']['entry_date'], 
                    'short_link':content['json_data']['short_link'],
                    'json_data':content['json_data']
                    }
            
            print("news lists => ",news)
            
            news_id = insert_news(cursor, title, content['content'], content['json_data']['entry_date'], content['json_data']['short_link'])
            print(f"Inserted news with ID {news_id}")
            
                        
            # print("\nnew no. => ",total)
            # print("title => ",title)
            # print("content => ",content['content'])
            # print("entry-date => ",content['json_data']['entry_date'])
            # # print("links => ",link)
            # print("short_link => ",content['json_data']['short_link'])
            
            # print("\n---------------------JSON ",total,"---------------------")
            # print("\njson => ",content['json_data'])  
            
            # print("\n---------------------DATE for CHECK---------------------")
            # date_format = '%A, %d %B %Y, %H:%M'
            # date_obj = datetime.strptime(entry_date, date_format)

            # print("datetime_convert => ",date_obj)
            
            # today = datetime.now().replace(microsecond=0)
            
            # future_date_30days = date_obj + timedelta(days=30)
            # print("future_date_30days => ",future_date_30days)
            
            # past_date_30days = date_obj - timedelta(days=30)
            # print("past_date_30days => ",past_date_30days)
            
            # print("---------------------END---------------------\n\n\n")
            

            
            
            
            
            
            ### Call Function Connect Database and Insert to PostgreSQL database ###                     
            
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
    
    
    
    
    
    

    





    
 
 
 



