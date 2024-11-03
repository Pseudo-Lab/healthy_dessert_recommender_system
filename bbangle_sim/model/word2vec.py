from typing import Dict
from gensim.models import Word2Vec
from .base import BaseModel
from utils.modelutil import Word2VecUtil

class Word2Vec(BaseModel):
    def __init__(self, cfg, model: Word2Vec):
        self.cfg = cfg
        self.model = model
        self.code = cfg.get('code', 'word2vec')
        self.version = cfg.get('version', '0.0.0')
        self.threshold = cfg.get('threshold', 0.5)
        self.topk = cfg.get('topk', 3)

    def fit(self):
        pass

    def predict(self, query_id:int, data:Dict[int, str]) -> Dict[int, float]:
        query = data[query_id]
        result = {}
        for key in data.keys():
            result[key] = Word2VecUtil.get_similarity(query, data[key], self.model)
        result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
        result = {k: result[k] for k in list(result)[1:1+self.topk] if result[k] > self.threshold}
        return result