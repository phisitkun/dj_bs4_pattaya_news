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


def get_content(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('p').text

    return content


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    news = {}
    for post in posts:
        # get content by post
        try:
            title = post.find('h3', attrs={"class":"entry-title"}).text
            # content = post.find('div',attrs={"class":"td-excerpt"}).text
            links = post.find('h3',attrs={"class":"entry-title"}).find('a').get('href')
            entrydate = post.find('time', class_='entry-date').text.strip()
            # json_data = {
            # 'title': title,
            # 'content': content,
            # 'link': link,
            # }
            
            # print(type(date_obj))
            
            content = get_content(links)
                        
            print("title => ",title)
            print("content => ",content)
            print("links => ",links)
            
            print("Today's date:", today)
            print("entry-date => ",entrydate)
            
            datetime_str = '09/21/22 13:55:26'
            date_format = '%A, %d %B %Y, %H:%M'

            date_obj = datetime.strptime(entrydate, date_format)

            print("datetime_convert => ",date_obj)

            
            today = datetime.now().replace(microsecond=0)
            
            future_date_30days = date_obj + timedelta(days=30)
            print("future_date_30days => ",future_date_30days)
            
            past_date_30days = date_obj - timedelta(days=30)
            print("past_date_30days => ",past_date_30days)
            
            print("---------------------END---------------------\n")
            
            title, content = get_content(links)
            # print("json_data => ",json_data)
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
 
 
 



