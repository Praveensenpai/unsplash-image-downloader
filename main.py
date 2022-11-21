import requests
from selectolax.parser import HTMLParser
import re
import wget
import os
from concurrent.futures import ThreadPoolExecutor


def get_download_urls(search_term: str = "dog") -> list[str]:
    r = requests.get(f"https://unsplash.com/s/photos/{search_term}")
    soup = HTMLParser(r.text)
    images = soup.css_first("[data-test='search-photos-route']").css("img")

    image_urls = []
    for img in images:
        if "srcset" in img.attributes:
            img = img.attributes["srcset"]
            img = re.search(pattern=r"https://.*?\?", string=img).group()[:-1]
            image_urls.append(img)
    return image_urls


def save_image(download_path: str, name: str, download_url: str) -> None:
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    file: str = os.path.join(download_path, f'{name}.png')
    wget.download(download_url, file)


def get_images(term: str, amount: int = None) -> None:
    if images := get_download_urls(search_term=term):
        if amount:
            images = images[:amount]
        max_workers = min(len(images), 20)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            [executor.submit(save_image, 'downloads', f'{term}-{i}', url)
             for i, url in enumerate(images)]

    else:
        print("No results found")


if __name__ == '__main__':
    get_images(term='dog', amount=10)
