import requests
from bs4 import BeautifulSoup

def main():
    response = requests.get('https://orenday.ru/news/', headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }, timeout=10)

    main_bs = BeautifulSoup(response.text, 'lxml')
    all_links = []
    all_links_bs = main_bs.find_all('a')
    for link_bs in all_links_bs:
        link = link_bs.get('href')
        if link.startswith('news/'):
            all_links.append('https://orenday.ru/'+link_bs['href'])
    print(all_links)

if __name__ == '__main__':
    main()