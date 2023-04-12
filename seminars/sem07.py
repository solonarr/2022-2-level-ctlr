import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://orenday.ru/news/040423085845'
    response = requests.get(url)
    #print(response.status_code)


    main_bs = BeautifulSoup(response.text, 'lxml')

    #title
    title_bs = main_bs.find_all('h1')
    print(title_bs[0].text)

    #date
    date_text = main_bs.find('span', {'itemprop':'datePublished'})
    date_bs = date_text.text
    print(date_bs)

    #author
    author_name = main_bs.find('div', {'class':'fright'})
    text_author = author_name.find('a', {'rel':'author'})
    print(text_author.text)

    #text
    article_text = main_bs.find('div', {'itemprop':'articleBody'})
    text_bs = article_text.find_all('p')
    for t in text_bs:
        print(t.text)




if __name__ == '__main__':
    main()