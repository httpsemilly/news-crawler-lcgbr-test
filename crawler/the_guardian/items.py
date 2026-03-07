import scrapy

class TheGuardianItem(scrapy.Item):
    """
    Class that represents a news article scraped from The Guardian website.
    
    Attributes:
        article_url: URL of the article.
        headline: Main title of the article.
        author: List of authors.
        article_text: Full body text of the article.
        published_date: Original publication date and time.
        category: The Guardian section (e.g. World, Politics).
        standfirst: Short summary displayed below the headline.
        scraped_at: Timestamp of when the article was collected.
    """

    article_url = scrapy.Field()
    headline = scrapy.Field()
    author = scrapy.Field()
    article_text = scrapy.Field()
    published_date = scrapy.Field()
    category = scrapy.Field()
    standfirst = scrapy.Field()
    scraped_at = scrapy.Field()