import requests
from bs4 import BeautifulSoup

url = 'https://cpython.uz/users/'
response = requests.get(url=url)
# print(response.status_code)
# print(response.text)

soup = BeautifulSoup(markup=response.text, features='lxml')
# print(soup.find(name='table', attrs={'id': 'rating'}))

qism1 = soup.find(name='table', id='rating')
qism2 = soup.find(name='table', id='rating').find(name='tbody')
qism3 = soup.find(name='table', id='rating').find(name='tbody').find(name='tr')
qism4 = soup.find(name='table', id='rating').find(name='tbody').find(name='tr').find_all('td')
qism5 = soup.find(name='table', id='rating').find(name='tbody').find_all(name='tr')
print("qism1 = ", qism1)
print("qism2 = ", qism2)
print("qism3 = ", qism3)
print("qism4 = ", qism4)
print("qism4[-1] = ", soup.find(name='table', id='rating').find(name='tbody').find(name='tr').find_all('td')[-1])
print("qism5 = ", qism5)

for page in range(1, 27):
    params = {'page': page}
    response = requests.get('https://cpython.uz/users/', params=params)
    soup = BeautifulSoup(response.text, 'lxml')
    qism5 = soup.find(name='table', id='rating').find(name='tbody').find_all(name='tr')
    for row in qism5:
        print(row.find_all(name='td')[1].find(name='span').text.strip(), row.find_all(name='td')[-1].find(name='span').text)