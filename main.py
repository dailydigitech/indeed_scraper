import requests
import os
from bs4 import BeautifulSoup

url = 'https://www.indeed.com/jobs?'
params = {
    'q': 'python developer',
    'l': 'newyork'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.0.0 Safari/537.36'}

req = requests.get(url)
print(req.status_code)


# soup = BeautifulSoup(res.text, 'html.parser')

# print(soup.prettify())

def get_total_pages():
    params = {
        'q': 'python developer',
        'l': 'newyork'
    }

    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w', encoding='utf-8') as outfile:
        outfile.write(res.text)
        outfile.close()

    # scraping step

    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.prettify())


if __name__ == '__main__':
    get_total_pages()
