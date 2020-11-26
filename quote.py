#!/usr/bin/env python3
# coding=utf-8

import sys
import requests
import json
from bs4 import BeautifulSoup
import argparse
import lxml
import cchardet
import time
import concurrent.futures

MAX_THREADS = 30

session = requests.Session()

def pagination():
    webpage = session.get(url)
    soup = BeautifulSoup(webpage.content,'lxml')
    page_numbers = soup.find("div",class_="quotes").find("div",attrs={"style":"text-align: right; width: 100%"})
    page_numbers = page_numbers.get_text().split()
    return range(int(page_numbers[-3])+1)

def get_quotes(quote_html):
    for quote in quote_html:
        quotes_list.append(quote_json(str(quote.get_text(strip=True))))

def quote_json(quote):
    quote_dir = quote.split("―")
    quote_author = quote_dir[1].split(',')
    quote_object = {
            "quote" : quote_dir[0],
            "author" : quote_author[0],
            "book" : quote_author[1] if len(quote_author) == 2 else ""
            }
    return (quote_object)

def resolvePage(pageno):
    webpage_url = url + "?page="+str(pageno)
    print(webpage_url)
    page = session.get(webpage_url)
    soup = BeautifulSoup(page.content,'lxml')
    #results = soup.find('div',class_="quotes")
    quote_html = soup.find_all('div',class_="quoteText")
    get_quotes(quote_html)

def resolvePages(pages):
#    for i in range(1,pages+1):
    threads = min(MAX_THREADS, len(pages))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(resolvePage, pages)

if __name__ == "__main__":
    quotes_list = []
    
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="Url of quotes page of author.")
    parser.add_argument("--output", help="output to txt file. usage --output [filename]")
    args = parser.parse_args()

    url = args.url
    
    if args.output:
        f = open(args.output+".txt", "w", encoding='utf-8')
    else:
        f = open("demo.txt", "w", encoding='utf-8')

    pages = pagination()
    resolvePages(pages)
    
    f.write(json.dumps(quotes_list, ensure_ascii=False, indent=4))
    f.close()
    
    print("Done\n")
