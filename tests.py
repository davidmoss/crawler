import pytest

from crawler import crawl_site, process_response, Page
from requests import Response


class TestCrawler:

    @pytest.mark.integration
    def test_crawl_site(self):
        index = crawl_site('http://www.davidcmoss.co.uk')
        expected_response = [
            Page(
                url=u'http://www.davidcmoss.co.uk/',
                title=['David C Moss'],
                links=set([
                    u'http://www.davidcmoss.co.uk/static/Curriculum Vitae.pdf']
                ),
                ex_links=set(['https://www.heroku.com']),
                images=['/static/img/profile.jpeg']),
            Page(
                url=u'http://www.davidcmoss.co.uk/static/Curriculum%20Vitae.pdf',
                title=[],
                links=set([]),
                ex_links=set([]),
                images=[])
        ]
        assert index == expected_response

    def test_process_response_links(self):
        host_url = 'http://www.davidcmoss.co.uk/'
        content = "<a href='/test' />"
        response = Response()
        response.url = host_url
        response._content = content
        page = process_response(host_url, response)
        assert host_url + 'test' in page.links

    def test_process_response_ex_links(self):
        host_url = 'http://www.davidcmoss.co.uk/'
        content = "<a href='http://google.com' />"
        response = Response()
        response.url = host_url
        response._content = content
        page = process_response(host_url, response)
        assert 'http://google.com' in page.ex_links

    def test_process_response_imgs(self):
        host_url = 'http://www.davidcmoss.co.uk/'
        content = "<img src='test.png' />"
        response = Response()
        response.url = host_url
        response._content = content
        page = process_response(host_url, response)
        assert 'test.png' in page.images
