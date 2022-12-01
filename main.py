import aiohttp
import asyncio
import time
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


async def check_http(url):
    allowed_methods = {}
    async with aiohttp.ClientSession() as session:
        http_methods = {
            'GET': lambda url: session.get(url),
            'POST': lambda url: session.post(url),
            'PUT': lambda url: session.put(url),
            'DELETE': lambda url: session.delete(url),
            'HEAD': lambda url: session.head(url),
            'PATCH': lambda url: session.patch(url),
            'OPTION': lambda url: session.options(url),
        }
        tasks = []
        for func in http_methods.values():
            response = asyncio.create_task(func(url))
            tasks.append(response)
        responses = await asyncio.gather(*tasks)
        result = tuple(zip(http_methods.keys(), (i.status for i in responses)))
        result = dict(filter(lambda x: x[1] != 405, result))
        allowed_methods[url] = result
        return allowed_methods


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
