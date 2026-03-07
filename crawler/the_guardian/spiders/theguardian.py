import scrapy
import re
from ..items import TheGuardianItem
from datetime import datetime

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
        excluded_sections = ['/audio/', '/live/', '/gallery/', 'info']

        for url in articles:
            if not any(section in url for section in excluded_sections):
                if re.search(pattern, url) != None:
                    yield response.follow(url, callback=self.parse_article)

    def parse_article(self, response):
        """
        Extracts structured data from each individual article page.

        Creates a instance of the class TheGuardianItem and fills each field using CSS selectors.

        Args:
            response: Scrapy response object from the individual article page.

        Yields:
            TheGuardianItem: A populated item containing the article structured data.
        """

        item = TheGuardianItem()

        item['headline'] = response.css('h1::text').get()
        item['article_url'] = response.url
        item['author'] = response.css('address[data-component="meta-byline"] a[rel="author"]::text').getall()
        item['article_text'] = " ".join(response.css('div#maincontent p::text').getall())
        item['published_date'] = response.css('details[data-gu-name="dateline"] summary span::text').get()
        item['category'] = response.url.split('/')[3]
        item['standfirst'] = response.css('div[data-gu-name="standfirst"] div p::text').get()
        item['scraped_at'] = datetime.now()

        yield item
