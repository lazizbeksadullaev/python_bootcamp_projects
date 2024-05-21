import requests
from googletrans import Translator
from pprint import pprint

tarjimon = Translator()


app_id = "4c6fa93e"
app_key = "5e79ca463391b8874fd220800e2b7c84"
language = "en-gb"


def get_definition(word_id):
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    res = r.json()
    if 'error' in res.keys():
        return False

    output = {}
    senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
    definitions = []

    k = 0
    for sense in senses:
        k = k + 1
        word_explanation = f"{k}. {sense['definitions'][0]}"
        try:
            word_explanation += f"\nExample: {sense['examples'][0]['text']}\n"
        except Exception:
            pass
        definitions.append(word_explanation)

    output['definitions'] = '\n'.join(definitions)

    if res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0].get('audioFile', False):
        output['audio'] = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']

    return output


if __name__ == '__main__':
    pprint(get_definition('execute'))
    print(get_definition('Americadf'))
    # print(type(tarjimon.detect('salom')))
    # print(tarjimon.detect('salom'))
    # print(tarjimon.detect('salom').lang)
    # print(tarjimon.detect('salom').confidence)

# meaning = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
# audio = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
# print("meaning = ", meaning)
# print("audio = ", audio)
# print("print(res) = ", res)
# print("print(r) = ", r)
# pprint(res)# faqat consoleda tushunarli qilib chiqarish uchun ishlatiladi, lekin shu chiroyli
# pprint(r)# qilish uchun qatordafi yozuvlarni pastga tushraman deb json ni dabdala qiladi
# shu sabab pprint()dan chiqgan json ni ishlatsa kopincha xato berdai
# bu holda print() dan chiqgan json ni ishlatish tavsiya etiladi
