import urllib.request


class HtmlUtil:
    @staticmethod
    def scrape_html_by_url(url):
        with urllib.request.urlopen(url) as response:
            html = response.read()
        return html

