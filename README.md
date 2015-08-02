# Crawler

This is a web crawler to generate a site map for your site

## Design

* Language choice = Python
    - library support & html parsers
    - Easy text processing
    - Easy to read and maintain
    - Non blocking I/O
    - Would consider Go as an alternative given time
* Librarys
    - lXML vs BeautifulSoup for parsing
    - grequests for concurrent requests
    - Scrapy great scalable, distributed crawler
    - Mechanize

* write tests
* Get all urls from page
* Record all urls found and queue up any new urls found
* Iterate through urls and build up index of pages and child pages
* Control the rate (concurrency) the page requests are made
* Build site map in HTML
* Remove achor links
* Breadth vs depth
* Group together external links and images
* Handle 429 (too many requests) status code

## TODO

* Obey robots.txt
* Handle larger number of urls with a bloom filter
* Mask operation with random user agent & private proxy
* Handle dynamic content AJAX content with PhantomJS
* Support command line argument to set the domain name to scrape

## Instructions

Prerequisites:

* Python 2.7
* Setuptools
* Virtualenv and Virtualenv-wrapper

Setup your virtualenv:

    $ mkvirtualenv crawler
    $ pip install -r requirments.txt

Run:

    $ python crawler.py

## Test

Run all tests:

    $ py.test tests.py

Run all unittests:

    $ py.test tests.py -v -m "not integration"