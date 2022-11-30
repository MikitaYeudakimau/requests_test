import asyncio
import time
import requests
import urlextract
import re


def check_name(string):
    sites = []
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
        sites.append(url)
    print(sites)
    return sites


async def check_response_status(url, method, func):
    # if method == "GET":
    #     try:
    #         response = await func(url, 5)
    #         # return response.status_code
    #         print(response.status_code)
    #     except:
    #         print(f"Check '{url}' for right spelling ")
    #         print('False')
    # else:
    response = func(url)
    print(f"Check method {method}")
    if response.status_code != 405:
        return (method, response.status_code)


async def check_http(url):
    http_methods = {
        'GET': lambda url: requests.get(url),
        'POST': lambda url: requests.post(url),
        'PUT': lambda url: requests.put(url),
        'DELETE': lambda url: requests.delete(url),
        'HEAD': lambda url: requests.head(url),
        'PATCH': lambda url: requests.patch(url),
        'OPTION': lambda url: requests.options(url),
    }
    response_tasks = []
    for method, func in http_methods.items():
        response_status = asyncio.create_task(check_response_status(url, method, func))
        response_tasks.append(response_status)
    result = await asyncio.gather(*response_tasks)
    allowed_methods = {}
    print(result)
    for res in result:
        if res != None:
            allowed_methods[res[0]] = res[1]
    dict = {}
    dict[url] = allowed_methods
    return dict
    print(dict)


async def parse(sites):
    tasks = []
    for site in sites:
        task = asyncio.create_task(check_http(site))
        tasks.append(task)
    res = await asyncio.gather(*tasks)
    print(res)


if __name__ == '__main__':
    sites = check_name(input("Введите URL через запятую: "))
    t1 = time.time()
    asyncio.run(parse(sites))
    elapsed = time.time() - t1
    print(f"Runtime time: {elapsed}")
