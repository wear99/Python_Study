import requests
from bs4 import BeautifulSoup

res = requests.get(url='https://blog.csdn.net/weixin_43499626/article/details/102967127')

bs = BeautifulSoup(res.text)


for x in bs.find_all('h2'):
    print(x)
    for y in bs.find_all('h3'):
        print('\t',y)
