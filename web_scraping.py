# from bs4 import BeautifulSoup
# import requests

# # HTML From File
# with open("index.html", "r") as f:
# 	doc = BeautifulSoup(f, "html.parser")

# tags = doc.find_all("p")[0]

# print(tags.find_all("b"))

# # HTML From Website
# url = "https://thepattayanews.com/2023/11/13/top-pattaya-news-from-the-last-week-pattaya-jazz-festival-soi-buakhao-road-to-be-converted-to-one-way-and-more/"

# result = requests.get(url)
# doc = BeautifulSoup(result.text, "html.parser")

# prices = doc.find_all(text="$")
# parent = prices[0].parent
# strong = parent.find("strong")
# print(strong.string)

from bs4 import BeautifulSoup

with open("index.html","r") as f:
    doc = BeautifulSoup(f, "html.parser")

print(doc.prettify())