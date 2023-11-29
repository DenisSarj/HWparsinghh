import time
import requests
import json
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_vacancy_python() -> list[dict]:
    url_hh = f'https://spb.hh.ru/search/vacancy?L_save_area=true&text=Python&search_field=name&search_field=company_name&search_field=description&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=50&page=0'

    headers = Headers(browser='Chrome', os='win').generate()

    response = requests.get(url_hh, headers=headers)

    soup = BeautifulSoup(response.content, 'lxml')
    vacancies = soup.find_all('div', class_='serp-item')

    data_list = []

    for vacancy in vacancies:

        title_tag = vacancy.find('a', class_='serp-item__title')
        href = title_tag.attrs['href']
        title = title_tag.text
        response2 = requests.get(f'{href}', headers=headers)

        time.sleep(0.4)

        city = 'Город не указан'
        soup2 = BeautifulSoup(response2.text, 'lxml')
        city_tag = soup2.find_all('div', class_='vacancy-section')

        for item in city_tag:
            i = item.find('h2')
            if i is not None and 'Адрес' in i:
                city = item.text.split(', ')[0].replace('Адрес', '')

        salary = 'Договорная заработная плата'
        salary_tag = soup2.find_all('div', class_='vacancy-title')

        for item in salary_tag:

            i = item.find('span', class_="bloko-header-section-2 bloko-header-section-2_lite")

            if i is not None:
                salary = i.text

        text_ = soup2.find('div', class_='g-user-content')
        p = text_.find_all('p')

        for items in p:

            text = items.text

            if 'Django' in text or 'Flask' in text:

                data_dict = {'ref': href, 'title': title, 'city': city, 'salary': salary}
                data_list.append(data_dict)

                break
    return data_list


if __name__ == '__main__':
    f = get_vacancy_python()
    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(f, file, ensure_ascii=False, indent=2)
