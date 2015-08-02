# -*- coding: utf-8 -*-
"""
Web crawler - generate your site map

@created: 01/08/2015
@author: davidmoss
"""
from __future__ import unicode_literals

import collections
import grequests
import urllib

from jinja2 import Environment, FileSystemLoader
from lxml import html
from urlparse import urljoin

HOST_URL = 'http://wiprodigital.com/'
OUTPUT_FILE = 'site_map.html'
CONCURRENCY = 1

Page = collections.namedtuple(
    'Page', ['title', 'links', 'ex_links', 'images']
)


def generate_html(index):
    """
    Generate HTML site map for site index
    """
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('site_map.html')
    return template.render(index=sorted(index.items()), site=HOST_URL)


def write_to_file(html, output_file):
    with open(output_file, "wb") as fh:
        fh.write(html.encode('utf-8'))


def process_response(host_url, response):
    """
    Extract the title, hrefs and imgs for the url response
    """
    body = html.fromstring(response.content)

    title = body.xpath('//title/text()')
    hrefs = body.xpath('//a/@href')
    imgs = body.xpath('//img/@src')

    if title:
        sub_str = (
            ' | Wipro Digital | An Innovation-Led,'
            ' Digital Transformation Partner'
        )
        title = title[0].replace(sub_str, '')

    # Finds all links from the site
    links = {urljoin(response.url, url)
             for url in hrefs
             if urljoin(response.url, url).startswith(host_url)
             and '#' not in url}

    # Finds all external links from the site
    ex_links = {urljoin(response.url, url)
                for url in hrefs
                if not urljoin(response.url, url).startswith(host_url)}

    # Build full urls for images
    images = {urljoin(response.url, img) for img in imgs}

    return Page(title=title, links=links,
                ex_links=sorted(ex_links), images=sorted(images))


def crawl_site(host_url):
    """
    Fetch all links from a site
    """
    urls_queue = collections.deque()
    urls_queue.append(host_url)

    found_urls = set()
    found_urls.add(host_url)

    index = {}

    while len(urls_queue):
        # Fetch many pages at once
        num_urls = min(len(urls_queue), CONCURRENCY)
        rs = (grequests.get(urls_queue.popleft()) for i in range(num_urls))
        responses = grequests.map(rs)

        for response in responses:
            # Get the links from the page
            if response.status_code == 200:
                page = process_response(host_url, response)

                # Set difference to find new URLs
                for link in (page.links - found_urls):
                    found_urls.add(link)
                    urls_queue.append(link)
            else:
                print "{} page returned status code {}".format(
                    response.url, response.status_code)
                urls_queue.append(response.url)

            index[urllib.unquote(response.url).decode('utf8')] = page

    return index


if __name__ == '__main__':
    # Use cmd args to pass in the domain to be crawled
    index = crawl_site(HOST_URL)
    index_html = generate_html(index)
    write_to_file(index_html, OUTPUT_FILE)
