import argparse
import requests
from bs4 import BeautifulSoup
import pandas as pd


def parsing(max, name):
    '''
    Функция для парсинга тендеров с сайта
    :param max: максимальное количество тендеров
    :param name: название сохраняемого csv-файла
    :return: флаг состояния выполнения функции
    '''

    tenders = []
    URL = "https://www.b2b-center.ru/market/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="table table-hover table-filled search-results")
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 0:
            return 0

        number_link_tag = cols[0].find("a")
        tender_name = number_link_tag.text.strip()
        tender_link = "https://www.b2b-center.ru" + number_link_tag["href"]
        organisation = cols[1].text.strip()
        publicated = cols[2].text.strip()
        end_date = cols[3].text.strip()

        tender = {
            'name': " ".join(tender_name.split()),
            'organisation': organisation,
            'publicated': publicated,
            'end_date': end_date,
            'link': tender_link
        }

        tenders.append(tender)

        if len(tenders) >= max:
            df = pd.DataFrame(tenders)
            df.to_csv(name, index=False, encoding="utf-8-sig")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Скачивает тендеры и сохраняет в файл")
    parser.add_argument("--max", type=int, default=20, help="Максимальное количество тендеров (по умолчанию 20)")
    parser.add_argument("--output", type=str, default="tenders.csv", help="Имя выходного файла CSV")

    args = parser.parse_args()
    res = parsing(args.max, args.output)

    if res == 0:
        print("Тендеры не были найдены.")
    else:
        print(f'Сохранено в {args.output}')