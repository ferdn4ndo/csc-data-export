import os
from MySQLdb import _mysql

from services.string.string_service import StringService


class DatabaseService:
    config: dict

    def __init__(self, config: [dict] = None):
        self.config = config if config is not None else self.read_config()

    @staticmethod
    def read_config():
        return {
            'user': os.getenv("DB_USER"),
            'password': os.getenv("DB_PASS"),
            'host': os.getenv("DB_HOST"),
            'database': os.getenv("DB_NAME"),
        }

    def create_connection(self):
        config = self.read_config()
        cnx = _mysql.connect(**config)

        return cnx

    def fetch_all_query_results(self, query: str, as_dict: bool = True) -> list:
        connection = self.create_connection()

        connection.query(query)
        result = connection.store_result()
        items = result.fetch_row(maxrows=0, how=1 if as_dict else 0)

        connection.close()

        return items

    def fetch_one_query_row(self, query: str, as_dict: bool = True) -> dict:
        items = self.fetch_all_query_results(query=query, as_dict=as_dict)

        return items[0] if len(items) > 0 else None

    def fetch_query_first_column(self, query: str) -> str:
        item = self.fetch_one_query_row(query=query, as_dict=False)

        return StringService.read_db_string(item[0], os.getenv('DB_ENCODING', 'utf-8'))
