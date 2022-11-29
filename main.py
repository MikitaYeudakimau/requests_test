import time

import requests
import urlextract
import re


# http_methods = {
#     'GET': requests.get(url),
#     'POST': requests.post(url),
#     'PUT': requests.put(url),
#     'DELETE': requests.delete(url),
#     'HEAD': requests.head(url),
#     'PATCH': requests.patch(url),
#     'OPTION': requests.options(url),
# }
def check_name(string):
    sites = {}
    lst = [i.strip(" ") for i in string.split(",")]
    for i in lst:
        url = i
        extractor = urlextract.URLExtract()
        urls = extractor.find_urls(url)
        if not urls:
            print(f"Строка {url} не является ссылкой")
            continue
        elif re.match(r'https?://', url) is None:
            print("URL введен некорректно")
            continue
        sites[url] = {}
    return sites

def check_http(dict):
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
    return dict

def parse(string):
    t1 = time.time()
    sites = check_name(string)
    dict = check_http(sites)
    t2 = time.time()
    dt = t2 - t1
    if dict:
        print(dict)
        print(dt)


if __name__ == '__main__':
    parse(input("Введите URL через запятую: "))
