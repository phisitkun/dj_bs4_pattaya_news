#### scrape_only ####

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import psycopg2
import re



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
# Get content from Link URL
##############################
#
def get_content_json(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', attrs={"class":"entry-title"}).text
    # content = soup.find('p').text
    content = soup.find_all(["h3", "p"])
    
    # Convert Array to String
    content_str = ''.join(map(str, content))
    
    content_final = remove_html_tags(content_str)
     
    json_data = {
            'title': title,
            'content': content_final,
            'link': link,
            }
    
    return_data = {
        'title' : title,
        'content' : content_final,
        'json_data' : json_data
    }
    
    return return_data



############################################################
# Function to check for newer news based on entry date
############################################################
#
def check_for_new_news(cursor, entry_date):
    query = "SELECT entry_date FROM news WHERE entry_date > %s"
    cursor.execute(query, (entry_date,))
    return cursor.fetchall()



############################################################
# Function to insert news into the PostgreSQL database
############################################################
#
def insert_news(cursor, title, content, entry_date, link):
    query = "INSERT INTO news (title, content, entry_date, link) VALUES (%s, %s, %s, %s) RETURNING id"
    cursor.execute(query, (title, content, entry_date, link))
    return cursor.fetchone()[0]

    
# Extract news information from the website
# news_entries = LIST for Insert to DATABASE

# Create a connection to the PostgreSQL database
connection = create_connection()
if connection:
    print("Database Connected!!")
    # with connection:
    #     with connection.cursor() as cursor:
    #         for entry in news_entries:
    #             # Extract information from the news entry
    #             title = entry.find('h2').text
    #             content = entry.find('p').text
    #             entry_date_str = entry.find('span', class_='entry-date').text
    #             entry_date = datetime.strptime(entry_date_str, '%Y-%m-%d').date()
    #             link = entry.find('a')['href']

    #             # Check if the news is newer than what is in the database
    #             newer_news = check_for_new_news(cursor, entry_date)

    #             if not newer_news:
    #                 # If the news is newer, insert it into the database
    #                 news_id = insert_news(cursor, title, content, entry_date, link)
    #                 print(f"Inserted news with ID {news_id}")
    #             else:
    #                 print("News already in the database")
                
    # return cursor.fetchone()[0]
    
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

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    total = 0
    for post in posts:
        # get content by post
        total = total+1
        try:
            
            title = post.find('h3', attrs={"class":"entry-title"}).text
            # content = post.find('div',attrs={"class":"td-excerpt"}).text
            links = post.find('h3',attrs={"class":"entry-title"}).find('a').get('href')
            entrydate = post.find('time', class_='entry-date').text.strip()
            
            content = get_content_json(links)
                        
            print("new no. => ",total)
            print("title => ",title)
            print("content => ",content['content'])
            print("entry-date => ",entrydate)
            print("links => ",links)
            
            print("\n---------------------JSON ",total,"---------------------")
            print("json => ",content['json_data'])  
            
            print("\n---------------------DATE for CHECK---------------------")
            date_format = '%A, %d %B %Y, %H:%M'
            date_obj = datetime.strptime(entrydate, date_format)

            print("datetime_convert => ",date_obj)
            
            today = datetime.now().replace(microsecond=0)
            
            future_date_30days = date_obj + timedelta(days=30)
            print("future_date_30days => ",future_date_30days)
            
            past_date_30days = date_obj - timedelta(days=30)
            print("past_date_30days => ",past_date_30days)
            
            print("---------------------END---------------------\n\n\n")
            
            title, content = get_content_json(links)
            # print("json_data => ",json_data)  
            
            ### Call Function Connect Database and Insert to PostgreSQL database ###
                        
            
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
    
    
    
    
    
    
    

    





    
 
 
 



