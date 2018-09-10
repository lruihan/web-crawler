import requests
from bs4 import BeautifulSoup
import codecs

# def douban_top_250():
#     for page in range(10):
#         url = 'https://movie.douban.com/top250?start=' + str(page * 25)
#         source_code = requests.get(url)
#         plain_text = source_code.text
#         soup = BeautifulSoup(plain_text, features="html.parser")
#         for link in soup.findAll('a'):
#             href = link.get('href')
#             title = link.string
#             print(href)
#             print(title)
#
# douban_top_250()

DOWNLOAD_URL = 'http://movie.douban.com/top250'

def download_page(url):
    #solution to Anti-Crawling
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    # }
    #data = requests.get(url, headers=headers).content
    data = requests.get(url).content
    return data

def main():
    url = DOWNLOAD_URL
    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write('{movies}\n'.format(movies='\n'.join(movies)))

def parse_html(html):

    soup = BeautifulSoup(html, features="html.parser")
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []

    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None

if __name__ == '__main__':
    main()