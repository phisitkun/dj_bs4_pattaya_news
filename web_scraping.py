import requests
from bs4 import BeautifulSoup

url = 'https://thepattayanews.com'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', class_='td-block-row')
    for post in posts:
        # get content by post
        title = post.find('h3', attrs={"class":"entry-title"}).text
        content = soup.find('div',attrs={"class":"td-excerpt"}).text
        links = soup.find('a',attrs={"class":"td-image-wrap"}).get('href')
        print(title)
        # print(content)
        print(links)
        print('\n\n')
        
else:
    print(f"Failed to fetch content. Status code: {response.status_code}")


