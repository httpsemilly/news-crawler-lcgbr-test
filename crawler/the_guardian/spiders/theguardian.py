import scrapy
import re
from ..items import TheGuardianItem
from datetime import datetime
from readability import Document
from bs4 import BeautifulSoup

class TheGuardianSpider(scrapy.Spider):
    """
    Spider for scraping news articles from The Guardian international page.
    
    Crawls the Guardian's international page, filters out non-article content
    such as liveblogs, audio and galleries, and extracts structured data from each article found.

    Extracts the following fields: headline, article_url, author, article_text,
    published_date, category, standfirst and scraped_at.

    Methods:
        parse(): Collects and filters article URLs from the Guardian's international page.
        parse_article(): Extracts structured data from each individual article page.
    """

    name = "theguardian"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/international"]

    def parse(self, response):
        """
        Collects and filters article URLs from The Guardian's international page.

        Filters out liveblogs, audio and gallery URLs, and follows only URLs
        that match the standard Guardian article pattern.

        Args:
            response: Scrapy response object from the international page.

        Yields:
            request: A Scrapy request for each valid article URL.
        """

        articles = response.css("a::attr(href)").getall()
        pattern = r"/\d{4}/[a-z]{3}/\d{2}/"
        excluded_sections = ['/audio/', '/live/', '/gallery/', '/info/', '/picture/', '/sign-up']

        for url in articles:
            if not any(section in url for section in excluded_sections):
                if re.search(pattern, url) is not None:
                    yield response.follow(url, callback=self.parse_article)

    def parse_article(self, response):
        """
        Extracts structured data from each individual article page.

        Creates a instance of the class TheGuardianItem and fills each field using CSS selectors and Readability.

        Args:
            response: Scrapy response object from the individual article page.

        Yields:
            TheGuardianItem: A populated item containing the article structured data.
        """

        item = TheGuardianItem()
        doc = Document(response.text)

        item['article_url'] = response.url

        item['headline'] = response.css('h1::text').get()
        if item['headline'] is None:
            item['headline'] = response.css('h1 span::text').get()

        item['author'] = response.css('a[rel="author"]::text').getall()
        if not item['author']:
            item['author'] = response.css('address[data-component="meta-byline"] div span::text').getall()

        item['article_text'] = BeautifulSoup(doc.summary(), 'lxml').get_text()

        item['published_date'] = response.css('details[data-gu-name="dateline"] summary span::text').get()

        if item['published_date'] is None:
            item['published_date'] = response.css('div[data-gu-name="dateline"]::text').get()

        if item['published_date'] is not None:
            item['published_date'] = datetime.strptime(item['published_date'], '%a %d %b %Y %H.%M %Z').strftime('%Y-%m-%d %H:%M:%S')

        item['category'] = response.url.split('/')[3]
        item['standfirst'] = response.css('div[data-gu-name="standfirst"] div p::text').get()
        item['scraped_at'] = datetime.now().replace(microsecond=0).isoformat()

        yield item