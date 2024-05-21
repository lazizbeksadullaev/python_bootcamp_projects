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
#

# class Quran():
#     def __init__(self, chapter, verse, text):
#         self.chapter = chapter
#         self.verse = verse
#         self.text = text
#
#     def __repr__(self):
#         return f"{self.text}"
#
#
# sura1 = Quran(chapter=1, verse=1, text= 'Меҳрибон ва раҳмли Аллоҳнинг номи билан бошлайман. (Аллоҳ таоло ўз китобини \"бисмиллаҳ\" билан бошлагани мусулмонларга ҳам ўрнак, улар ҳам доим ўз сўзларини ва ишларини \"бисмиллаҳ\" билан бошламоқлари лозим. Пайғамбар алайҳиссалом ҳадисларидан бирида: \"Эътиборли ҳар бир иш \"бисмиллаҳ\" билан бошланмас экан, унинг охири кесикдир\", деганлар. Яъни, баракаси бўлмайди, охирига етмайди)')
# print(sura1)