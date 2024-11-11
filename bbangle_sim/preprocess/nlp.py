
import re
from typing import List, Set
import pandas as pd 

class NaturalLangPreProcessor:

    def __init__(self):
        pass

    def change_case(self, df: pd.DataFrame, case: str='lower', **kwargs) -> pd.DataFrame:
        for column in kwargs.get('columns', []):
            if case == 'lower':
                df[column] = df[column].str.lower()
            elif case == 'upper':
                df[column] = df[column].str.upper()
        return df
    
    def remove_stopwords(self, df: pd.DataFrame, stopwords:Set[str], **kwargs) -> pd.DataFrame:
        for column in kwargs.get('columns', []):
            df[column] = df[column].apply(lambda x: ' '.join([word for word in x.split() if word not in stopwords]))
        return df

    def remove_pattern(self, df: pd.DataFrame, pattern:str, **kwargs) -> pd.DataFrame:
        compiler = re.compile(pattern)
        for column in kwargs.get('columns', []):
            df[column] = df[column].apply(lambda x: compiler.sub('', x))
        print(df['title'])
        return df

    def fill_nan(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        for column in kwargs.get('columns', []):
            df[column] = df[column].fillna('')
        return df
    
    def make_soup(self, df: pd.DataFrame, **kwargs) -> pd.DataFrame:
        cols = kwargs.get('columns', [])
        df['description'] = df[cols].apply(lambda x: ' '.join(x), axis=1)
        return df
        
