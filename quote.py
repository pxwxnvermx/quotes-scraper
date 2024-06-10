#!/usr/bin/env python3
# coding=utf-8

import argparse
import json
import asyncio
import logging
import sys

import httpx
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

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
    return range(1, page_numbers[-1] + 1)


def quote_json(quote_text):
    quote, quote_info = quote_text.split("―")
    author, *book = quote_info.split(",")
    return dict(quote=quote, author=author, book="".join(book))


async def resolve_page(page_url, client):
    page = await client.get(page_url)
    soup = BeautifulSoup(page.content, "lxml")
    quote_html = [
        quote.get_text(strip=True) for quote in soup.find_all("div", class_="quoteText")
    ]
    return list(map(quote_json, quote_html))



async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url of quotes page of author.")
    parser.add_argument(
        "--output", help="output to txt file. usage --output [filename]"
    )
    args = parser.parse_args()
    filename = args.output + ".json" if args.output else "quotes.json"

    async with httpx.AsyncClient() as client:
        logging.info("Fetching page numbers")
        page1 = await client.get(args.url)
        page_numbers = get_pagination_range(page1)
        logging.info(f"Total pages to fetch: {page_numbers[-1]}")
        quotes = await asyncio.gather(*[resolve_page(f"{args.url}?page={num}", client) for num in page_numbers])
        logging.info(f"Fetch done")
    
    with open(filename, "w", encoding="utf-8") as f:
        logging.info(f"Saving to File {filename}")
        f.write(json.dumps(quotes, ensure_ascii=False, indent=4))
    logging.info("Finished")


if __name__ == "__main__":
    asyncio.run(main())
