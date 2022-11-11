import requests
import os
from dotenv import load_dotenv
import argparse
from urllib.parse import urlparse


def shorten_link(token, long_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "long_url": long_url
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json() ["link"]


def count_clicks(token, user_url):
    parsed_url = urlparse(user_url)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["total_clicks"]


def is_bitlink(token, user_url):
    parsed_url = urlparse(user_url)
    bitlink = f"{parsed_url.netloc}{parsed_url.path}"
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Сокращает ссылку или считает клики'
    )
    parser.add_argument('link', help='Ваше ссылка')
    args = parser.parse_args()
    load_dotenv()
    bitly_token = os.environ["BITLY_TOKEN"]
    user_url = args.link
    try:
        if is_bitlink(bitly_token, user_url):
            print('клики', count_clicks(bitly_token, user_url))
        else:
            print('Битлинк', shorten_link(bitly_token, user_url))
    except requests.exceptions.HTTPError:
        print("Извините,но к сожалению ваша ссылка некорректна")
