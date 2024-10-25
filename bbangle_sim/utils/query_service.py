from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

class QueryService:
    def __init__(self, cfg):
        self.cfg = cfg
        self.user_name = cfg['user_name']
        self.password = quote_plus(cfg['password'])
        self.host = cfg['host']
        self.port = cfg['port']
        self.schema = cfg['schema']
        self.engine = self.connect()

    def connect(self):
        return create_engine(f"mysql+pymysql://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.schema}")

    def query_to_pandas_df(self, query):
        return pd.read_sql(query, self.engine)
        

