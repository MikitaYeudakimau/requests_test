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
    return sites


async def check_response_status(url, method, func):
    if method == "GET":
        try:
            response = func(url, 5)
            # return response.status_code
            print(response.status_code)
        except:
            print(f"Check '{url}' for right spelling ")
            print('False')
    # else:
    #     response = func(url)
    #     if response.status_code != 405:
    #         return response.status_code
    #     else:
    #         return None


async def check_http(url):
    http_methods = {
        'GET': lambda url, timeout: requests.get(url, timeout=timeout),
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
    print(result)
    # if response_status is False:break
    # elif response_status is True:
    #     dict[url][method] = response_status
    # print(dict)


async def parse(string):
    t1 = time.time()
    sites = check_name(string)
    print(sites)
    tasks = []
    for site in sites:
        task = asyncio.create_task(check_http(site))
        tasks.append(task)
    await asyncio.gather(tasks)
    # checked_dict = {k: v for k, v in dict.items() if v != {}}
    print(f"Runtime time: {time.time() - t1}")


if __name__ == '__main__':
    asyncio.run(parse(input("Введите URL через запятую: ")))
