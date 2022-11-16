import requests
import urlextract
import re


def parse():
    dict = {}
    n = input("Введите количество передаваемых строк: ")
    if n.isdigit():
        n = int(n)
    else:
        print("Некорректный ввод количества строк")
        return None
    for i in range(n):
        url = input("Введите URL: ")
        extractor = urlextract.URLExtract()
        urls = extractor.find_urls(url)
        if not urls:
            print(f"Строка {url} не является ссылкой")
            continue
        elif re.match(r'https?://', url) is None:
            print("URL введен некорректно")
            continue
        dict[url] = {}
    for url in dict.keys():
        response = requests.get(url)
        if response.status_code != 405:
            dict[url]['GET'] = response.status_code
        response = requests.post(url)
        if response.status_code != 405:
            dict[url]['POST'] = response.status_code
        response = requests.put(url)
        if response.status_code != 405:
            dict[url]['PUT'] = response.status_code
        response = requests.delete(url)
        if response.status_code != 405:
            dict[url]['DELETE'] = response.status_code
        response = requests.head(url)
        if response.status_code != 405:
            dict[url]['HEAD'] = response.status_code
        response = requests.patch(url)
        if response.status_code != 405:
            dict[url]['PATCH'] = response.status_code
        response = requests.options(url)
        if response.status_code != 405:
            dict[url]['OPTIONS'] = response.status_code
    if dict:
        print(dict)


parse()
