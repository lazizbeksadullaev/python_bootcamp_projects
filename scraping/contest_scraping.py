import requests
from bs4 import BeautifulSoup

for contest_id in range(1, 2):
    url = f"https://cpython.uz/competitions/contests/contest/213/standings/"
    response = requests.get(url=url)
    soup = BeautifulSoup(markup=response.text, features='lxml')
    if (table := soup.find(name='table', attrs={'id': 'standings'})):
        # print(table.find(name='tbody').find(name='tr').find(name='p', attrs={"class": "text-center"}).parent.contents)
        for tr in table.find('tbody').find_all(name='tr'):
            print(tr.find(name='td', attrs={"class":"td-content"}).find(name='p', attrs={"class": "text-center"}).string)