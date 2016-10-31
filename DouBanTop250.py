#!usr/bin/env python
# encoding=utf-8
import codecs
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250'


def get_html(url, params=None):
    data = requests.get(url, params=params).content
    return data


def parse_html(html):
    bs = BeautifulSoup(html, 'html.parser')
    movies = []
    movie_list = bs.find('ol', attrs={'class', 'grid_view'})
    for li in movie_list.find_all('li'):
        detail = li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).get_text()
        movies.append(movie_name)
    next_page = bs.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movies, DOWNLOAD_URL + next_page['href']
    return movies, None


def main():
    url = DOWNLOAD_URL
    with codecs.open('MoviesTop250.txt', 'wb', encoding='utf-8') as f:
        count = 1
        while url:
            html = get_html(url)
            movies, url = parse_html(html)
            for movie in movies:
                f.write('{}{}{}{}'.format(str(count), '.', movie, '\r\n'))
                count += 1


if __name__ == '__main__':
    main()
