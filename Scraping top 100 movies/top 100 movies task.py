from bs4 import BeautifulSoup
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
soup = BeautifulSoup(response.text, "html.parser")

movies = []
for i in soup.find_all('h3',attrs={'class':'title'}):
    movies.insert(0,i.text)
# print(len(movies))
with open('top 100 movies.txt','w', encoding='utf-8') as file:
    for i in movies:
        file.write(i+'\n')