import pandas as pd
import warnings
import re 
from model.bow import BagOfWords
from model.tfidf import TfIdf
import yaml
import matplotlib.pyplot as plt

from utils.preprocessing import *
from konlpy.tag import Okt
from datetime import datetime

warnings.filterwarnings("ignore")



#### Configuration
# - 추천 서비스 생성을 위해서 필요한 설정값들을 세팅합니다.

# config
with open('configs/database.yaml') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

from utils.query_service import QueryService
query_service = QueryService(cfg['mysql'])


#### Data Import
# - 사용할 데이터를 mysql에서 가져옵니다. 


PRODUCT_BOARD_SQL = """
SELECT id
, store_id
, title
, price
, is_soldout
, view
, purchase_url 
FROM product_board
"""
product_board = query_service.query_to_pandas_df(PRODUCT_BOARD_SQL)


PRODUCT_SQL = """
SELECT id
, product_board_id
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


#### Preprocessing
# - Product + Product board + Review 데이터 기반 유사도 테이블
# - 평가 방법 3가지 수행 및 시각화
# - 품절된 상품 후처리 고려

sold_out = product_board[product_board['is_soldout']==1]['store_id'].unique()

grouped = product.groupby('product_board_id').agg({
    'id': 'first',
    'option': ' '.join, # option을 공백을 두고 이어 붙임
    'option_price': 'first',
    'category': 'first',
    'gluten_free_tag': 'first',
    'high_protein_tag': 'first',
    'sugar_free_tag': 'first',
    'vegan_tag': 'first',
    'ketogenic_tag': 'first',
})


df = grouped.copy()
df['id'] = df.index
df.shape


grouped = review.groupby('board_id').agg({
    'rate': 'mean',
    'content': ' '.join  # content을 공백을 두고 이어 붙임
})


df_review = grouped.copy()
df_review['id'] = df_review.index


df = df[['id', 'option', 'option_price', 'category', 'gluten_free_tag', 'high_protein_tag', 'sugar_free_tag', 'vegan_tag', 'ketogenic_tag']].copy()
df['option'] = df['option'].fillna('')
df.loc[df['option'] == '필수상품 없음', 'option'] = ''


# 두 데이터프레임을 store_id (df_board)와 product_board_id (df) 기준으로 병합
merged_df = pd.merge(df, product_board, left_on='id', right_on='id', how='left')
merged_df = pd.merge(merged_df, df_review, left_on = 'id', right_on='id', how='left')
df = merged_df.copy()

# Create the new soup feature
df['title_content'] = df.apply(create_title, axis=1)

# title에 공백 추가
df['title_with_spaces'], df['title_nouns_list'] = zip(*df['title_content'].apply(add_spaces))
features = ['gluten_free_tag', 'high_protein_tag', 'sugar_free_tag', 'vegan_tag', 'ketogenic_tag']

for feature in features:
  df[feature] = df[feature].apply(lambda x: x*feature)

# Removes spaces and converts to lowercase
# Apply the generate_list function to cast, keywords, and director
for feature in ['category', 'gluten_free_tag', 'high_protein_tag', 'sugar_free_tag', 'vegan_tag', 'ketogenic_tag']:
    df[feature] = df[feature].apply(sanitize)

# Create the new soup feature
df['soup'] = df.apply(create_soup, axis=1)

#### Modeling(CountVec+TF-IDF)
# - Ranking Aggregation

### Modeling(CountVec)

# TfIdfVectorizer 가져오기
from sklearn.feature_extraction.text import TfidfVectorizer

# 불용어를 english로 지정하고 tf-idf 계산
# stop_words='english' 옵션은 영어의 불용어(예: the, and, is 등)를 제외
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['title_with_spaces'])

# Cosine 유사도 계산, overview기반으로 영화간 유사도 계산
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim_tf = cosine_similarity(tfidf_matrix, tfidf_matrix)
cosine_sim_tf = pd.DataFrame(cosine_sim_tf, index=df.index, columns=df.index)

### Modeling(TF-IDF)

# Import CountVectorizer from the scikit-learn library
from sklearn.feature_extraction.text import CountVectorizer

# Define a new CountVectorizer object and create vectors for the soup
count = CountVectorizer(stop_words='english')
# 상품*해당 단어가 있는지 카운트 벡터
count_matrix = count.fit_transform(df['soup'])

# Cosine 유사도 계산
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim_cv = cosine_similarity(count_matrix, count_matrix)
cosine_sim_cv = pd.DataFrame(cosine_sim_cv, index=df.index, columns=df.index)

cosine_sim_cv.shape

### Ranking Aggregation
import numpy as np
final_ranking = (np.argsort(cosine_sim_tf) + np.argsort(cosine_sim_cv)) / 2


### Recommendation Module

# Index에 product_board_id 추가
df['product_board_id'] = df['id'].copy()

# index-product_board_id을 뒤집는다
indices = pd.Series(df.index, index=df['product_board_id'])

# 상품제목을 받아서 추천 영화를 돌려주는 함수
def content_recommender_rank(product_board_id, n_of_recomm, final_ranking, sold_out):
    # product_board_id에서 영화 index 받아오기
    idx = indices[product_board_id]
    # 주어진 상품과 다른 상품의 similarity를 가져온다
    final_ranking_ = pd.DataFrame(final_ranking)
    final_ranking_ = final_ranking_[idx]
    # sold_out 후처리
    final_ranking_[sold_out] = 0
    # similarity 기준으로 정렬 
    final_ranking_ = final_ranking_.sort_values(ascending=True)[1:n_of_recomm+1]

    # 상품 product_board_id 반환    
    return [df.loc[final_ranking_.index]['product_board_id'].values, final_ranking_.values, df.loc[final_ranking_.index]['store_id'].values]




#### Evaluation
# 1. 같은 스토어 상품 추천 비율
# 2. Coverage
# 3. 추천 상품 정성 평가 (추천 상품 출력 -> 유사한지 확인)

### 1. 같은 스토어 상품 추천 비율

# 같은 스토어 상품 추천 개수
recommended_stores = []
recommended_stores_ = []

for i in df.product_board_id.values:
    recommended_stores_ = []
    test = content_recommender_rank(i, 3, final_ranking,sold_out)
    recommended_stores_.extend(test[2])
    recommended_stores.extend([1 for store_id in recommended_stores_ if store_id == i])
    
    
print(sum(recommended_stores)/len(df.product_board_id.values)*3*100,"%")


### 2. Coverage

recommended_items = []

for i in df.product_board_id.values:
    test = content_recommender_rank(i, 3, final_ranking, sold_out)
    recommended_items.extend(test[0])


recommended_items = list(map(lambda x: int(x), recommended_items))

from metrics.coverage import get_coverage

n_items = cosine_sim.shape[0]

get_coverage(recommended_items, n_items)


### 3. 추천 상품 정성 평가 (추천 상품 출력 -> 유사한지 확인)

total = []

for i in df.product_board_id.values:
    case_1, _, _ = content_recommender_rank(i, 3, final_ranking, sold_out)

    filtered_row = df.loc[df['product_board_id'] == i, ['product_board_id', 'store_id', 'title', 'purchase_url']]
    # query 길이에 맞게 해당 행을 여러 번 출력
    repeated_rows = pd.concat([filtered_row] * 3, ignore_index=True)
    repeated_rows = repeated_rows.reset_index(drop=True)
    repeated_rows.columns = ['query_item', 'query_store_id', 'query_title', 'query_purchase_url']
    
 
    recommended_results = df.loc[df['product_board_id'].isin(case_1), ['product_board_id', 'store_id', 'title', 'purchase_url']]
    recommended_results = recommended_results.reset_index(drop=True)
    recommended_results.columns = ['recommendation_item', 'recommendation_store_id', 'recommendation_title', 'recommendation_purchase_url']
    

    #print(recommended_results)


    part = pd.concat([repeated_rows, recommended_results], axis = 1)

    if len(total) == 0:
        total = part.copy()
    else:
        total = pd.concat([total, part], axis = 0)


    
print(total.shape)

total.to_csv('./Bow-1+TF-IDF with rank aggregation (voting).csv', index = False, encoding='utf-8-sig')


#### Save
# - 추천 결과 저장 

# query item
query_item = df.index.values.repeat(3)

# recommended_items
recommended_items = []

for i in df.product_board_id.values:
    test = content_recommender_rank(i, 3, final_ranking, sold_out)
    recommended_items.extend(test[0])


recommended_items = list(map(lambda x: int(x), recommended_items))

# score
score = []

for i in df.product_board_id.values:
    test = content_recommender_rank(i, 3, final_ranking, sold_out)
    score.extend(test[1])


score = list(map(lambda x: float(x), score))

# rank
rank = [1, 2, 3]*cosine_sim.shape[0]
# recommendation item title
recommendation_theme = ['similarity']*cosine_sim.shape[0]*3
# model_version
model_version = ['bow-1+TF-IDF']*cosine_sim.shape[0]*3
# created at
created_at = [datetime.now()]*cosine_sim.shape[0]*3
# modified_at
modified_at = [datetime.now()]*cosine_sim.shape[0]*3


import pandas as pd
from datetime import datetime
data = {
    'query_item': query_item,
    'recommendation_item': recommended_items,
    'score': score,
    'rank': rank,
    'recommendation_theme': recommendation_theme,
    'model_version': model_version,
    'created_at': created_at,
    'modified_at': modified_at
}

recommendation_df = pd.DataFrame(data)


recommendation_df.to_csv('recommendation_for_product_page.csv'+str(datetime.now()), index = False)