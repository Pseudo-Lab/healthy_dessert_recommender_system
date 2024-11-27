import yaml
from konlpy.tag import Okt
from utils.query_service import QueryService
from model.default import DefaultModel
from utils.modelutil import Word2VecUtil
from model.word2vec import Word2Vec
from preprocess.nlp import NaturalLangPreProcessor
from generator.generator import RecommendationGenerator
import pandas as pd 

# config
with open('configs/database.yaml') as f:
    database_cfg = yaml.load(f, Loader=yaml.FullLoader)
with open('configs/service.yaml') as f:
    service_cfg = yaml.load(f, Loader=yaml.FullLoader)

with open('data/stopwords.txt', 'r',  encoding='utf-8') as f:
    stopwords = f.readlines()
    stopwords = set(x.strip() for x in stopwords)

# Query Service 
query_service = QueryService(database_cfg['mysql'])

nlp_preprocessor = NaturalLangPreProcessor()
tokenizer = Okt()
PRODUCT_BOARD_SQL = """
SELECT id as board_id
, store_id 
, title
, price
, is_soldout
, purchase_url
, view 
FROM product_board
"""
product_board = query_service.query_to_pandas_df(PRODUCT_BOARD_SQL)


PRODUCT_SQL = """
SELECT id as product_id
, product_board_id as board_id
, title as option
, price as option_price
, category
, gluten_free_tag
, high_protein_tag
, sugar_free_tag
, vegan_tag
, ketogenic_tag
FROM product
"""
product = query_service.query_to_pandas_df(PRODUCT_SQL)
product = product.groupby('board_id').agg({'option': lambda x: ' '.join(x)})


REVIEW_SQL = """
SELECT board_id 
, badge_taste
, badge_brix
, badge_texture
, rate
, content
FROM review
"""
review = query_service.query_to_pandas_df(REVIEW_SQL)
review = review.drop_duplicates(subset=['board_id', 'content'], keep='first')
review = review.groupby('board_id').agg({'content': lambda x: ' '.join(x)})

df = (product_board
 .merge(product, on='board_id', how='left')
 .merge(review, on='board_id', how='left')
)[['board_id', 'title', 'option', 'content']]

df = nlp_preprocessor.fill_nan(df, columns=['title', 'option', 'content'])
df = nlp_preprocessor.change_case(df, case='lower', columns=['title', 'option', 'content'])
df = nlp_preprocessor.remove_pattern(df, pattern=r'\d+[개입|kg|팩|개|종|입|원|g]+', columns=['title', 'option', 'content'])
df = nlp_preprocessor.remove_pattern(df, pattern=r'[^가-힣0-9a-zA-Z\s]', columns=['title', 'option', 'content'])
df = nlp_preprocessor.remove_stopwords(df, stopwords=stopwords, columns=['title', 'option', 'content'])
df = nlp_preprocessor.make_soup(df, columns=['title', 'option', 'content'])

df['token'] = df['description'].apply(lambda x: tokenizer.morphs(x))
df['unique_token'] = df['token'].apply(lambda x: list(set(x)))
df['description'] = df['token'].apply(lambda x: ' '.join(x))
df.set_index('board_id', inplace=True)
data = df['description'].to_dict()

# Model 
default_model = DefaultModel(service_cfg['model']['default'])
word2vec_model_path = "word2vec/korean_word2vec_model.model"  
word2vec_model = Word2VecUtil.load_model(word2vec_model_path)
word2vec = Word2Vec(service_cfg['model']['word2vec'], word2vec_model)

# Generator
generator = RecommendationGenerator(service_cfg, word2vec, default_model)


def main():
    rec_result = generator.generate(data)
    rows = []
    for query, result in rec_result.items():
        key = query
        for i, (k, v) in enumerate(result['items'].items()):
            row = {
                'query_item': key,
                'recommendation_item': k,
                'score': v,
                'rank': i+1,
                'recommendation_theme': result['recommendation_theme'],
                'model_version': result['model_version']
            }
            rows.append(row)
    result_df = pd.DataFrame(rows)
    result_df['created_at'] = pd.Timestamp.now(tz='Asia/Seoul') 
    result_df['modified_at'] = pd.Timestamp.now(tz='Asia/Seoul')
    result_df.to_csv('data/recommendation_result.csv', index=False)
    return result_df 


if __name__ == '__main__':
    result_df = main()
    print(result_df)