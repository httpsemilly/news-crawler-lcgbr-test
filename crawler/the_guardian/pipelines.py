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
        """Initializes the BigQuery client and table reference when the spider opens."""

        config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'config.yaml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        self.dataset = config['bigquery']['dataset']
        self.table = config['bigquery']['table']

        self.client = bigquery.Client()

        self.dataset_ref = self.client.dataset(self.dataset)
        self.table_ref = self.dataset_ref.table(self.table)

    def process_item(self, item):
        """
        Inserts a scraped article item into BigQuery.

        Args:
            item: A TheGuardianItem instance containing the article data.

        Returns:
            item: The item after successful insertion.

        Raises:
            Exception: If BigQuery returns errors during row insertion.
        """

        item = ItemAdapter(item).asdict()
        errors = self.client.insert_rows_json(self.table_ref, [item])

        if errors:
            raise Exception(f"Encountered errors while inserting rows: {errors}")
        
        return item