#### scrape_only ####

import psycopg2
import re
import requests
import validators
import json
import cloudinary.uploader
import pandas as pd
from bs4 import BeautifulSoup
from django.contrib.gis.db import models
from datetime import date, datetime, timedelta
from cloudinary import CloudinaryImage, uploader
from cloudinary.models import CloudinaryField
from django_better_admin_arrayfield.models.fields import ArrayField

cloudinary.config( 
  cloud_name = "dbvevdrrr", 
  api_key = "647799521524182", 
  api_secret = "vzE_C_Bo3E5i0MkI5yZSb3szqqM", 
  secure = True
)

def image_url(image):
    if image is None:
        return f"https://res.cloudinary.com/dbvevdrrr/image/upload/v1700725539/No_Image_Available_revtfe.jpg"
    else:
        return f"https://res.cloudinary.com/dbvevdrrr/{image}"


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
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)




############################## 
# Function Convert Datetime
##############################
#
def convert_datetimestamp(var_date):
    date_format = "%A, %d %B %Y, %H:%M"
    date_obj = datetime.strptime(var_date, date_format)
    datetimestamp = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return datetimestamp



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
# Function Upload News images
##############################
#
def news_images(image_url):
    
        if validators.url(image_url):
            try:
                img_url = uploader.upload(image_url)
                return img_url["public_id"]
            except:
                pass
        else:
            pass
        



##############################
# Get content from Link URL
##############################
#
def get_content_json(link):
    
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1", attrs={"class":"entry-title"}).text
    short_link = soup.find("link",{"rel":"shortlink"}).get("href")
    img_new = soup.find("img", attrs={"class":"entry-thumb"})["src"]
    entry_date = soup.find("time", class_="entry-date").text.strip()
    datetimestamp = convert_datetimestamp(entry_date)
    
    is_duplicated = False
    table_name = 'scraper_pagecontent'
    primary_key = 'url'
    data_frame = ''  ### data from beautiful soup
    
    
    # iframe = soup.find("div", attrs={"class":"epyt-video-wrapper"}).text
    iframe = soup.find('iframe')
    iframe.extract() ### avoid iframe tag
    
    content = soup.find_all(["h3", "p"])

    # Check content
    if (content != None):
        try:
            content = content
        except:
            pass
    else:
        pass
    
    # print("before check_duplicates() call",short_link)

    # Check for duplicates
    is_duplicated = check_duplicate_data(connection, short_link)  ### get short_link check duplicate in DB
    if(is_duplicated):
        print("News is duplicated ",short_link)
    else:    
        print("News is not duplicated ",short_link)
        #### upload image to cloudodinary
        # pic_upload_id = news_images(img_new) 
        # img_new = str(pic_upload_id)
        # print("img_new cloudodinary => ",img_new)
    
    
    # Convert Array to String
    content_str = "".join(map(str, content))
    
    content_final = remove_html_tags(content_str)
    
    
    
    # date_format = "%A, %d %B %Y, %H:%M"
    # date_obj = datetime.strptime(entry_date, date_format)
    # datetimestamp = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    
    obj_data = {
            "title": title,
            "img_url" : img_new,
            "short_link": short_link,
            "content": content_final,
            "entry_date": datetimestamp,
            }
    if(is_duplicated):
        json_data = ''
    else :
        json_data = convert_to_json(obj_data)  
    
    
    return json_data



############################################################
# Function to insert news into the PostgreSQL database
############################################################
#
def insert_news(cursor, short_link="", title="", content="", img_url="", json={}, entry_date=datetime):
    
    print("\n---------------------insert ",total,"---------------------")
    
    query = "INSERT INTO scraper_pagecontent (url, title, content, img_url, json, entry_date) VALUES (%s, %s, %s, %s, %s, %s) RETURNING title,url"
    # cursor.execute(query, (short_link, title, content, img_url, json, entry_date))
    
    
    try:
        cursor.execute(query, (short_link, title, content, img_url, json, entry_date))
    except Exception as err: ### show error detail
        print ("Oops! An exception has occured:", err)
        print ("Exception TYPE:", type(err))
        
    
    
    connection.commit()
    
    return cursor.fetchone()









def check_duplicate_data(connection, short_link):
    # print("input short_link => ",short_link)
    connection = create_connection()
    # Read data from PostgreSQL into a DataFrame
    query = "SELECT url FROM public.scraper_pagecontent ORDER BY id ASC;"
    df_postgres = pd.read_sql(query, connection)
    # print("Check df_postgres  => ",df_postgres)

    # Extract relevant data from the HTML (adjust as per your HTML structure)
    extracted_data = {
        'url': short_link
        # Add more keys and extraction logic as needed
    }

    # Convert extracted data to a DataFrame
    df_extracted = pd.DataFrame([extracted_data])

    # Check for duplicates based on the 'url' column
    is_duplicate = any(df_postgres['url'].isin(df_extracted['url']))

    # print("Check is_duplicate in func => ",is_duplicate)
    # Close the database connection
    connection.close()

    return is_duplicate





############################################################
# Function to check for duplicate data in PostgreSQL
# data_frame is data list for check duplicate
############################################################
#

# def check_duplicates(connection, table_name, primary_key, short_link):
#     # Assuming 'connection' is a psycopg2 connection object
#     print("check_duplicates() call ",short_link)

#     # Concatenate primary key columns to check for duplicates
#     query = f"SELECT {primary_key} FROM {table_name};"
    
#     connection = create_connection()
#     sql_query = "SELECT url FROM public.scraper_pagecontent ORDER BY id ASC "
    
#     # existing_data = pd.read_sql_query(query, connection) ### get all lists data from DB
#     # print("existing_data => ",existing_data)

#     # Check for duplicates
#     duplicates = data_frame[data_frame.duplicated(subset=primary_key, keep=False)]
#     print("duplicates return => ",duplicates)

#     if not duplicates.empty:
#         print("Duplicate data found. Aborting further actions.")
#         return False

#     return True



###########################################
##### Start Get Info from Website URL #####
###########################################
#

# Create a connection to the PostgreSQL database
connection = create_connection()
cursor = connection.cursor()
    
    
url = "https://thepattayanews.com"
response = requests.get(url)
today = date.today()
news_entries = {} # Variable for news insert to DB

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    # posts = soup.find_all("div", class_="td-block-row")
    limit = 5 ##### add limit parameter limit result #####
    posts = soup.find_all('h3',class_='entry-title', limit=limit)    ### limit result (, limit=limit) 
    total = 0
    news_all = {}
    
    

    for post in posts:
        # get content by post
        anchor_element = post.find('a')
        link = anchor_element.get('href')
        
        total = total+1
        try:
            
            json_str = get_content_json(link)  ### return json string
            # print("\n json_str return => ",json_str)  
            
            
            
            # print("\ndisplay data before insert => ",news)
            
            ##### Insert data if no duplicates
            if(json_str): ### check duplicate data from DB is TRUE / FALSE
                news = json.loads(json_str)    ### return object
                
                news_res = insert_news(cursor, news["short_link"], news["title"], news["content"], news["img_url"], json_str, news["entry_date"])
                print("\n---------------------JSON ",total,"---------------------")
                print("\n insert news => ",news_res[0])  
                print("\n short_link news => ",news_res[1])  
            else :
                print("\n Not Insert News is Duplicated")  
            # Close the connection
            # print("---------------------END---------------------\n\n\n")
             
            
            ### Call Function Connect Database and Insert to PostgreSQL database ###                     
            
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    

connection.close() 
    
    
    
    
    

    





    
 
 
 



