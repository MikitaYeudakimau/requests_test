import time

import requests
import urlextract
import re


def check_name(string):
    sites = {}
    lst = [i.strip(" ") for i in string.split(",")]
    for i in lst:
        url = i
        extractor = urlextract.URLExtract()
        urls = extractor.find_urls(url)
        if not urls:
            print(f"String {url} isn't right link")
            continue
        elif re.match(r'https?://', url) is None:
            print("URL is written uncorrectly")
            continue
        sites[url] = {}
    return sites


def check_response_status(url, method, func):
    if method == "GET":
        try:
            response = func(url, 5)
        except:
            print(f"Check '{url}' for right spelling ")
            return False
    else:
        response = func(url)
        if response.status_code != 405:
            return response.status_code
        else:
            return None


def check_http(dict):
    http_methods = {
        'GET': lambda url, timeout: requests.get(url, timeout=timeout),
        'POST': lambda url: requests.post(url),
        'PUT': lambda url: requests.put(url),
        'DELETE': lambda url: requests.delete(url),
        'HEAD': lambda url: requests.head(url),
        'PATCH': lambda url: requests.patch(url),
        'OPTION': lambda url: requests.options(url),
    }
    for url in dict.keys():
        for method, func in http_methods.items():
            response_status = check_response_status(url, method, func)
            if response_status is False:
                break
            elif response_status is None:
                continue
            dict[url][method] = response_status
    return dict


def parse(string):
    t1 = time.time()
    sites = check_name(string)
    dict = check_http(sites)
    checked_dict = {k: v for k, v in dict.items() if v != {}}
    if checked_dict:
        print(checked_dict)
        print(f"Runtime time: {time.time() - t1}")


if __name__ == '__main__':
    parse(input("Введите URL через запятую: "))
