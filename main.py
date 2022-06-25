import requests
import json
import os
import pandas as pd
from bs4 import BeautifulSoup

site = 'https://www.indeed.com'
url = 'https://www.indeed.com/jobs?'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.0.0 Safari/537.36'}


def check_website():
    req = requests.get(url)
    print(f'status : {req.status_code}')
    # soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.prettify())


def get_total_pages(query, location):
    params = {
        'q': query,
        'l': location
    }
    res = requests.get(url, params=params, headers=headers)

    try:
        os.mkdir('temp')
    except FileExistsError:
        pass

    with open('temp/res.html', 'w+', encoding='utf-8') as outfile:
        outfile.write(res.text)
        outfile.close()

    # scraping step
    total_pages = []
    soup = BeautifulSoup(res.text, 'html.parser')
    soup.prettify()
    pagination = soup.find('ul', 'pagination-list')
    # print(pagination)
    pages = pagination.find_all('li')
    for page in pages:
        total_pages.append(page.text)
    # print(total_page)

    total = int(max(total_pages))
    # print(f'total page : {total}')
    return total


def get_all_items(query, location, start, page):
    params = {
        'q': query,
        'l': location,
        'start': start
    }

    res = requests.get(url, params=params, headers=headers)

    with open('temp/res.html', 'w+', encoding='utf-8') as outfile:
        outfile.write(res.text)
        outfile.close()
    soup = BeautifulSoup(res.text, 'html.parser')

    # scraping process
    contents = soup.find_all('table', 'jobCard_mainContent big6_visualChanges')

    job_list = []
    for item in contents:
        title = item.findNext('h2', 'jobTitle').text
        company = item.findNext('span', 'companyName')
        company_name = company.text
        try:
            company_link = site + company.findNext('a')['href']
        except:
            company_link = 'link is not available'

        # sorting Data
        data_dict = {
            'title': title,
            'company name': company_name,
            'link': company_link
        }
        # print(data_dict)

        job_list.append(data_dict)

    # print data
    # print('amount of data : ', len(job_list))
    # print(job_list)

    # writing json file
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass
    with open(f'json_result/{query}_in_{location}_page_{page}.json', 'w+') as json_data:
        json.dump(job_list, json_data)
    print('json created')
    return job_list


def create_document(dataframe, filename):
    try:
        os.mkdir('data_result')
    except FileExistsError:
        pass

    df = pd.DataFrame(dataframe)
    df.to_csv(f'data_result/{filename}.csv', index=False)
    df.to_excel(f'data_result/{filename}.xlsx', index=False)
    print(f'File {filename}.csv and {filename}.xlsx successfully created')


def run():
    query = input('query : ')
    location = input('location : ')

    total = get_total_pages(query, location)
    counter = 0
    final_result =[]

    for page in range(total):
        page += 1
        counter += 10
        final_result += get_all_items(query, location, counter, page)

    # formatting data
    try:
        os.mkdir('reports')
    except FileExistsError:
        pass
    with open('reports/{}.json'.format(query), 'w+') as final_data:
        json.dump(final_result, final_data)
    print('json created')

    # create_document
    create_document(final_result, query)


if __name__ == '__main__':
    run()