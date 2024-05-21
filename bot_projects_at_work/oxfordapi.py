import requests
import json
from pprint import pprint

app_id = "4c6fa93e"
app_key = "5e79ca463391b8874fd220800e2b7c84"
language = "en-gb"
word_id = "apple"
url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
print(r.status_code)
res = r.json()
meaning = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
# example = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text']
audio = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
print("meaning = ", meaning)
# print("example = ", example)
print("audio = ", audio)
print("print(res) = ", res)
print("print(r) = ", r)
pprint(res)# faqat consoleda tushunarli qilib chiqarish uchun ishlatiladi, lekin shu chiroyli
pprint(r)# qilish uchun qatordafi yozuvlarni pastga tushraman deb json ni dabdala qiladi
# shu sabab pprint()dan chiqgan json ni ishlatsa kopincha xato berdai
# bu holda print() dan chiqgan json ni ishlatish tavsiya etiladi