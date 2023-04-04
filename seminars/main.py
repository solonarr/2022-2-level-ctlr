import random

import requests
from bs4 import BeautifulSoup


def main():
    response = requests.get('https://orenday.ru/news/', headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }, timeout=10)

    print(response.status_code)

    with open('index.html', 'w', encoding='utf-8') as f:
         f.write(response.text)

    main_bs = BeautifulSoup(response.text, 'lxml')

    title_bs = main_bs.title
    print(title_bs.text)
    print(title_bs.name)
    print(title_bs.attrs)

    all_links_bs = main_bs.find_all('a')
    print(len(all_links_bs))

    all_links=[]
    for link_bs in all_links_bs:
        link = link_bs.get('href')
        if link is None: #no ==
            continue
        elif link[0] == 'n' and link[1] == 'e' and link[2] == 'w' and link.count('/')==1:
            all_links.append(link_bs['href'])
    print(all_links)





if __name__ == '__main__':
    main()

