#### scrape_only ####

from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from cloudinary import CloudinaryImage, uploader
import psycopg2
import re
import requests
import validators
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
    img_url = soup.find('img', attrs={"class":"entry-thumb"})['src']
    content = soup.find_all(["h3", "p"])
    entry_date = post.find('time', class_='entry-date').text.strip()
    
    # Check content
    if (content != None):
        try:
            content = content
        except:
            pass
    else:
        pass
        
    # Check image URL
    if img_url != None:
        if validators.url(img_url):
            try:
                img_url = uploader.upload(img_url)
                img_url = img_url["public_id"]
            except:
                pass
        else:
            pass
    
    # Convert Array to String
    content_str = ''.join(map(str, content))
    
    content_final = remove_html_tags(content_str)
    
    date_format = '%A, %d %B %Y, %H:%M'
    date_obj = datetime.strptime(entry_date, date_format)
    
    datetimestamp = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    
    obj_data = {
            'title': title,
            'img_url' : img_url,
            'short_link': short_link,
            'content': content_final,
            'entry_date': datetimestamp,
            }
    
    print("\njson_data => ",obj_data)
    
    json_data = convert_to_json(obj_data)  
    
    return json_data





############################################################
# Function to insert news into the PostgreSQL database
############################################################
#
def insert_news(cursor, short_link, title, content, img_url, json, entry_date):
    query = "INSERT INTO scraper_pagecontent (url, title, content, img_url, json, entry_date) VALUES (%s, %s, %s, %s, %s, %s) RETURNING title"
    cursor.execute(query, (short_link, title, content, img_url, json, entry_date))
    
    connection.commit()
    
    return cursor.fetchone()[0]

# Create a connection to the PostgreSQL database
connection = create_connection()

cursor = connection.cursor()




###########################################
##### Start Get Info from Website URL #####
###########################################
#
url = 'https://thepattayanews.com'
response = requests.get(url)
today = date.today()
news_entries = {} # Variable for news insert to DB

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
            link = post.find('h3',attrs={"class":"entry-title"}).find('a').get('href')
            entry_date = post.find('time', class_='entry-date').text.strip()
            
            json_data = get_content_json(link)
            news = json.loads(json_data)
            
            news = {
                    'title':news['title'], 
                    'content':news['content'], 
                    'img_url':news['img_url'], 
                    'entry_date':news['entry_date'], 
                    'short_link':news['short_link'],
                    'json_data':json_data,
                    }
            
            
            news_title = insert_news(cursor, news['short_link'], news['title'], news['content'], news['img_url'], json_data, news['entry_date'])
            

            
            
            print("\nadd News ",total," title => ",news_title)
            
                        
            # print("\nnew no. => ",total)
            # print("title => ",title)
            # print("content => ",json_data['content'])
            # print("entry-date => ",json_data['entry_date'])
            # # print("links => ",link)
            # print("short_link => ",json_data['short_link'])
            
            # print("\n---------------------JSON ",total,"---------------------")
            # print("\njson => ",content['json_data'])  
            
            # print("---------------------END---------------------\n\n\n")
             
            
            ### Call Function Connect Database and Insert to PostgreSQL database ###                     
            
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
    
    
    
    
    
    

    





    
 
 
 



