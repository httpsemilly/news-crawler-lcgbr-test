from itemadapter import ItemAdapter
from google.cloud import bigquery
import yaml
import os

class TheGuardianPipeline:
    """
    Pipeline for storing scraped articles into BigQuery.

    Connects to BigQuery on spider_open and inserts each scraped article into the configured dataset and table.

    Methods:
        open_spider(): Initializes the BigQuery client and table reference when the spider opens.
        process_item(): Inserts a scraped article item into BigQuery.
    """

    def open_spider(self):
        """Initializes the BigQuery client, creates the dataset and table if they don't exist,
        and sets up the table reference when the spider opens."""

        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        self.dataset = config['bigquery']['dataset']
        self.table = config['bigquery']['table']

        self.client = bigquery.Client()

        self.dataset_obj = bigquery.Dataset(f"{self.client.project}.{self.dataset}")
        self.client.create_dataset(self.dataset_obj, exists_ok=True)

        schema = [
            bigquery.SchemaField("headline", "STRING"),
            bigquery.SchemaField("article_url", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("author", "STRING", mode="REPEATED"),
            bigquery.SchemaField("article_text", "STRING"),
            bigquery.SchemaField("published_date", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("standfirst", "STRING"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_obj = bigquery.Table(f"{self.client.project}.{self.dataset}.{self.table}", schema=schema)
        self.client.create_table(table_obj, exists_ok=True)

        self.dataset_ref = self.client.dataset(self.dataset)
        self.table_ref = self.dataset_ref.table(self.table)

    def process_item(self, item):
        """
        Inserts a scraped article item into BigQuery.

        Args:
            item: A TheGuardianItem instance containing the article data.

        Returns:
            item: The scraped item, regardless of whether it was inserted or skipped.

        Raises:
            Exception: If BigQuery returns errors during row insertion.
        """

        item = ItemAdapter(item).asdict()

        query = f"SELECT COUNT(*) FROM `{self.dataset}.{self.table}` WHERE article_url = '{item['article_url']}'"
        result = self.client.query(query).result()
        count = list(result)[0][0]

        if count == 0:
            errors = self.client.insert_rows_json(self.table_ref, [item])
            if errors:
                raise Exception(f"Encountered errors while inserting rows: {errors}")
        
        return item