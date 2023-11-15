#### scrape_only ####

import requests
from bs4 import BeautifulSoup

url = 'https://thepattayanews.com'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    news = []
    for post in posts:
        # get content by post
        try:
            title = post.find('h3', attrs={"class":"entry-title"}).text
            content = post.find('div',attrs={"class":"td-excerpt"}).text
            links = post.find('h3',attrs={"class":"entry-title"}).find('a').get('href')
            print("title => ",title)
            print("content => ",content)
            print("links => ",links)
            print('\n\n')
        except:
                pass
        
        # Insert scraped data into the database
        # news.append(title)
        # news.append(content)
        # news.append(content)
        
        print(news)
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")
    
 
 
 
 
    
# #### scrape_and_insert ####   
    
# import requests
# from bs4 import BeautifulSoup
# # from PageContent.models import ScrapedContent
# from django.core.exceptions import ObjectDoesNotExist

# def scrape_and_insert():
#     url = 'https://thepattayanews.com'
#     response = requests.get(url)
#     news = []

# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     posts = soup.find_all('div', class_='td-block-row')
#     for post in posts:
#         # get content by post
#         title = post.find('h3', attrs={"class":"entry-title"}).text
#         content = soup.find('div',attrs={"class":"td-excerpt"}).text
#         links = soup.find('a',attrs={"class":"td-image-wrap"}).get('href')
#         # print(title)
#         # print(content)
#         # print(links)
#         # print('\n\n')

#         # Insert scraped data into the database
#         news.append(title)
#         news.append(content)
#         news.append(content)
    
#     print(news)

# if __name__ == '__main__':
#     scrape_and_insert()


