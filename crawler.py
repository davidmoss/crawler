# -*- coding: utf-8 -*-
"""
Web crawler - generate your site map

@created: 01/08/2015
@author: davidmoss
"""
from __future__ import unicode_literals

import collections
import grequests
from lxml import html
from urlparse import urljoin

HOST_URL = 'http://wiprodigital.com/'
CONCURRENCY = 5

Page = collections.namedtuple(
    'Page', ['url', 'title', 'links', 'ex_links', 'images']
)


def process_response(host_url, response):
    body = html.fromstring(response.content)

    title = body.xpath('//title/text()')
    hrefs = body.xpath('//a/@href')
    imgs = body.xpath('//img/@src')

    # Finds all links from the site
    links = {urljoin(response.url, url)
             for url in hrefs
             if urljoin(response.url, url).startswith(host_url)}

    # Finds all external links from the site
    ex_links = {urljoin(response.url, url)
                for url in hrefs
                if not urljoin(response.url, url).startswith(host_url)}

    return Page(url=response.url, title=title, links=links,
                ex_links=ex_links, images=imgs)


def crawl_site(host_url):
    """
    Fetch all links from a site
    """
    urls_queue = collections.deque()
    urls_queue.append(host_url)

    found_urls = set()
    found_urls.add(host_url)

    index = []

    while len(urls_queue):
        # Fetch many pages at once
        num_urls = min(len(urls_queue), CONCURRENCY)
        rs = (grequests.get(urls_queue.popleft()) for i in range(num_urls))
        responses = grequests.map(rs)

        for response in responses:
            # Get the links from the page
            page = process_response(host_url, response)

            # Set difference to find new URLs
            for link in (page.links - found_urls):
                found_urls.add(link)
                urls_queue.append(link)

            index.append(page)

    return index


if __name__ == '__main__':
    # Use cmd args to pass in the domain to be crawled
    index = crawl_site(HOST_URL)
