import requests

url = 'https://httpbin.org/get?key1=value1&key2=value2'
headers = {'user-agent': 'Google Chrome 92.0.4515.107'} #oxforda shunday edi
response = requests.get(url, headers=headers)
print("response.url = ", response.url)
print("response.json() = ", response.json())
print("response = ", response)
print("response.headers = ", response.headers)
print("response.ok = ", response.ok)

url = 'https://httpbin.org/get'
params = {'key1': 'value1', 'key2': 'value2'}
response1 = requests.get(url, params=params)
print("response1.url = ", response1.url)
print("response1.text = ", response1.text)

image_url = 'https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Cython-logo.svg/440px-Cython-logo.svg.png'
response = requests.get(image_url)

with open('python.png', 'wb') as image:
    image.write(response.content)

