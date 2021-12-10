#!/bin/python
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"}


def tryget(list, index):
    try:
        return list[index]
    except IndexError:
        return None


def get_url(id):
    r = requests.get(f"https://apkfind.com/store/download?id={id}", headers=HEADERS)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return "https:"+soup.select(".mdl-button")[0].get("href")


def download(url, path):
    if path in ['.', '']:
        path = f"./{url.split('/')[-1].split('?')[0]}"
    r = requests.get(url, headers=HEADERS, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f, tqdm(total=int(r.headers.get('content-length', 0)),
                                     unit='iB', unit_scale=True, unit_divisor=1024) as bar:
        for data in r.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)


if __name__ == "__main__":
    from sys import argv
    if (id := tryget(argv, 1)) is None or tryget(argv, 2) is None:
        exit("Usage: python main.py <id> <path>")
    if "https://play.google.com/store/apps/details" in id:
        id = id.split("id=")[1]
    print(f'Downloading {id}...')
    url = get_url(id)
    print(f"Got the download link: {url}\nDownloading...")
    download(url, argv[2])
