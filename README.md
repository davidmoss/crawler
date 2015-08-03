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

* Write tests
* Get all urls from page
* Record all urls found and queue up any new urls found
* Iterate through urls and build up index of pages and child pages
* Control the rate (concurrency) the page requests are made
* Build site map in HTML
* Remove achor links
* Breadth vs depth
* Group together external links and images
* Handle 429 (too many requests) status code

## Tradeoffs

Whilst implementing the solution I had to firstly choose the language to base this on. I chose python for 2 reasons, firstly it was my most comfortable language to work with at present and felt it had equally supportive libraries for doing text manipulation. This may not have been the fastest choice of language but for implementation and maintainability I felt it was a very valid choice.

I chose to use as standard and effcient libraries as possible to ensure that the implementation was as faster as possbile. This quickly led to the choice to use lxml and the requests library. I then wanted to explore trying to run multiple threads in parallel to split the task into smaller chunks that could make the extraction quicker. I chose to make mutliple requests to the site at the same time rather than a whole url analyse as I wanted to maintain a central list of urls scraped. This led to the popping mechanism of urls to fetch and the use of grequests to make multiple requests in parallell. Unfortunately though this started encountering 409's from the server which blocked too many requests from the source. The number of concurrent requests thus had to be scaled back to 1 or 2 to avoid too many failures having to be retried. This wasn't ideal and thus I would have potentially explored a more iterative approach.

There were a few additional tasks that would have made good stretch goals and help improve the functionality of the script.

## TODO

* Obey robots.txt
* Extract other static content - css, js, etc
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
