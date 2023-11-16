#### scrape_only ####

import requests
from bs4 import BeautifulSoup
from datetime import date,datetime
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
    # Extract content based on the HTML structure of the WordPress blog

    # Example: Extracting post title
    title = post.find('h1', class_='post-title').text.strip()

    # Example: Extracting post content
    content = post.find('p', class_='post-content').text.strip()
    # entrydate = post.find('time', class_='entry-date').text.strip()
    
    print("title => ",title)
    print("content => ",content)
    
    


    return title, content


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    news = {}
    for post in posts:
        # get content by post
        try:
            title = post.find('h3', attrs={"class":"entry-title"}).text
            content = post.find('div',attrs={"class":"td-excerpt"}).text
            links = post.find('h3',attrs={"class":"entry-title"}).find('a').get('href')
            entrydate = post.find('time', class_='entry-date').text.strip()
            # json_data = {
            # 'title': title,
            # 'content': content,
            # 'link': link,
            # }
            
            # print("title => ",title)
            # print("content => ",content)
            # print("links => ",links)
            # print("Today's date:", today)
            print("entry-date => ",entrydate)
            
            datetime_str = '09/21/22 13:55:26'
            date_format = '%Y-%m-%d %H:%M:%S'

            datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            print(type(datetime_object))
            print("datetime_object => ",datetime_object.strftime("%A, %d %B %Y, %H:%M"))  # printed in default format

            
            print("---------------------END---------------------\n")
            
            title, content = get_content(links)
            # print("json_data => ",json_data)
        except:
                pass
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
 
 
 



