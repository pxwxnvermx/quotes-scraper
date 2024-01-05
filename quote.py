#!/usr/bin/env python3
# coding=utf-8

import argparse
import json
import logging
from time import sleep

import httpx
from bs4 import BeautifulSoup


def get_pagination_range(page):
    soup = BeautifulSoup(page.content, "lxml")
    quote_div = soup.find("div", class_="quotes")
    if not quote_div:
        raise Exception()
    page_numbers = list(
        map(
            int,
            filter(
                lambda x: x.isdigit(),
                quote_div.find("div", class_="u-textAlignRight").get_text().split(),
            ),
        )
    )
    # only need pages from 2nd page as the first page is fetched already
    return range(2, page_numbers[-1] + 1)


def quote_json(quote_text):
    quote, quote_info = quote_text.split("―")
    author, *book = quote_info.split(",")
    return dict(quote=quote, author=author, book="".join(book))


def resolve_page(page):
    soup = BeautifulSoup(page.content, "lxml")
    quote_html = [
        quote.get_text(strip=True) for quote in soup.find_all("div", class_="quoteText")
    ]
    return list(map(quote_json, quote_html))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url of quotes page of author.")
    parser.add_argument(
        "--output", help="output to txt file. usage --output [filename]"
    )
    args = parser.parse_args()
    filename = args.output + ".json" if args.output else "demo.json"
    with httpx.Client() as client:
        page1 = client.get(args.url)
        page_numbers = get_pagination_range(page1)
        page_urls = list(f"{args.url}?page={num}" for num in page_numbers)
        pages = [page1]
        for url in page_urls:
            print(f"getting url {url}")
            pages.append(client.get(url))
            sleep(1)
        quotes = list(map(resolve_page, pages))

    with open(filename, "w", encoding="utf-8") as f:
        logging.info("writing to file")
        f.write(json.dumps(quotes, ensure_ascii=False, indent=4))
    logging.info("done")


if __name__ == "__main__":
    main()
