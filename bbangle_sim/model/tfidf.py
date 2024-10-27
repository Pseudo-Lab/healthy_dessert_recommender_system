from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from numpy import ndarray
from .base import BaseModel
from typing import List, Tuple, Union

class TfIdf(BaseModel):

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer
        self.vectorizer = TfidfVectorizer(tokenizer=self.tokenizer)
        self.cosine_matrix = None

    def fit(self, text: Union[list[str], ndarray]) -> None:
        tf_idf_matrix = self.vectorizer.fit_transform(text)
        self.cosine_matrix = cosine_similarity(tf_idf_matrix, tf_idf_matrix)

    def predict(self, idx: int, candidiate_top_k: int =10)->List[Tuple[int, float]]:
        sim_scores = list(enumerate(self.cosine_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) 
        sim_scores = sim_scores[1:candidiate_top_k+1] 
        return sim_scores






