
"""
Assignment 1 :  ABDUL GHAFFAR
install these packages for environment.
~apt-get install python
~apt-get install -y python3-pip
~pip3 install requests
~pip3 install bs4
"""

import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from os import path
from pathlib import PurePath
import logging

#create and configure logger 
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename= "scrapURLs.log", level= logging.DEBUG, format = LOG_FORMAT, filemode='w')
logger = logging.getLogger()

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

visited_urls = 0

def check_validation(url):
    """
    Checks whether `url` is a valid URL.
    """
    logger.info("Check valid url: {0}".format(url))
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def fetch_all_url_links(url):
    """
    Returns those URLs which belong to the same website
    """
    logger.info("Get All website links: {0}".format(url))
    # to get all URLs in url
    urls = set()
    # URL domain name without the protocol
    domain_name = urlparse(url).netloc
    # parse the url to beatifulSoup package
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    logger.debug("# search for the urls")
    #search for the url tags
    for tag_a in soup.findAll("a"):
        href = tag_a.attrs.get("href")
        # check for empty tag
        if href == "" or href is None:
            continue
        # join the relative URL
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not check_validation(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print("[!] External link:", href)
                external_urls.add(href)
            continue
        print("[*] Internal link:", href)
        urls.add(href)
        internal_urls.add(href)
    return urls


def creep(url, maximum_urls_number=30):
    """
    searches a web page and extracts all links.
    params:
        maximum_urls_number (int): number of max urls to creep, default is 30.
    """
    global visited_urls
    visited_urls += 1
    links = fetch_all_url_links(url)
    for link in links:
        if visited_urls > maximum_urls_number:
            break
        creep(link, maximum_urls_number=maximum_urls_number)


def extract(file_with_links):
    """
    Extract the contents from the urls present in the file.
    params:
        file_with_links (string): file name which contains the available urls.
    """
    logger.info("Extract the file containing the links, file: {0}".format(file_with_links))
    logger.debug("# opening file with links to write")

    with open(file_with_links, 'r') as file_handle:
        urls = file_handle.readlines()
    urls = [url.strip() for url in urls]  # strip `\n`

    for url in urls:
        file_name = PurePath(url).name
        file_path = path.join('.', file_name)
        text = ''
        print("url:: ", url)
        logger.debug("# check whether the request exists in the url")
        try:
            response = requests.get(url)
            if response.ok:
                text = response.text
        except requests.exceptions.ConnectionError as exception_handle:
            print(exception_handle)

        with open(file_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(text)

        print('Written to', file_path)

if __name__ == "__main__":

    url = input("Enter the url:: ")
    #url = 'https://www.google.com/'
    maximum_urls_number = 2

    creep(url, maximum_urls_number=maximum_urls_number)

    domain_name = urlparse(url).netloc

    # save the internal links to a file
    internalLinks = domain_name+"_internal_links.txt"
    externalLinks =domain_name+"_external_links.txt" 

    logger.debug("# opening file having internal links")

    with open(internalLinks, "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    logger.debug("# opening file having external links")

    # save the external links to a file
    with open(externalLinks, "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)
    extract(internalLinks)
    extract(externalLinks)
