#### scrape_only ####

import requests
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import json
import os
import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pattaya_news.settings')
# django.setup()
# from scraper.models import News

url = 'https://thepattayanews.com'
response = requests.get(url)
today = date.today()

# get content form link url
def get_content_json(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('h1', attrs={"class":"entry-title"}).text
    content = soup.find('p').text
    
    json_data = {
            'title': title,
            'content': content,
            'link': link,
            }
    
    return_data = {
        'title' : title,
        'content' : content,
        'json_data' : json_data
    }
    
    return return_data


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    news = {}
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
            
            title, content = get_content(links)
            # print("json_data => ",json_data)
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
 
 
 



