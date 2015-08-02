import os
import pytest

from crawler import (
    crawl_site, generate_html, process_response, Page, write_to_file
)
from requests import Response


class TestCrawler:

    @pytest.mark.integration
    def test_crawl_site(self):
        index = crawl_site('http://www.davidcmoss.co.uk')
        expected_response = {
            u'http://www.davidcmoss.co.uk/': Page(
                title=u'David C Moss',
                links=set([u'http://www.davidcmoss.co.uk/static/Curriculum Vitae.pdf']),
                ex_links=['https://www.heroku.com'],
                images=[u'http://www.davidcmoss.co.uk/static/img/profile.jpeg']
            ),
            u'http://www.davidcmoss.co.uk/static/Curriculum Vitae.pdf': Page(
                title=[],
                links=set([]),
                ex_links=[],
                images=[]
            )
        }
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
        assert host_url + 'test.png' in page.images

    def test_generate_html(self):
        index = {
            'http://www.davidcmoss.co.uk/':
            Page(
                title=['David C Moss'],
                links=set([
                    u'http://www.davidcmoss.co.uk/static/Curriculum Vitae.pdf']
                ),
                ex_links=set(['https://www.heroku.com']),
                images=['/static/img/profile.jpeg']),
            'http://www.davidcmoss.co.uk/static/Curriculum%20Vitae.pdf':
            Page(
                title=[],
                links=set([]),
                ex_links=set([]),
                images=[])
        }
        html = generate_html(index)
        assert "https://www.heroku.com" in html

    def test_write_to_file(self):
        html = '<body></body>'
        output_file = 'test.html'

        # ensure output file doesn't already exist
        if os.path.exists(output_file):
            os.removed(output_file)

        write_to_file(html, output_file)
        with open(output_file) as fh:
            result = fh.read()

        assert result == html
