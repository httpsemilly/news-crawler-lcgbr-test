from fastapi import FastAPI
from google.cloud import bigquery
import yaml
import os

config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

app = FastAPI()
client = bigquery.Client()

dataset = config['bigquery']['dataset']
table = config['bigquery']['table']

@app.get("/articles")
def search_articles(keyword: str):
    """
    Search for a keyword in the articles' headline or text.

    Args:
        keyword: The term to be searched.

    Returns:
        list: A list of articles matching the keyword, each one containing headline, article_url,
        author, published_date, category and standfirst. 
    """

    query = f"""SELECT headline, article_url, author, published_date, category, standfirst 
    FROM `{dataset}.{table}` 
    WHERE LOWER(headline) LIKE '%{keyword.lower()}%' OR LOWER(article_text) LIKE '%{keyword.lower()}%'
    """

    result = client.query(query).result()
    articles = []

    for article in result:
        articles.append(dict(article))
    
    return articles