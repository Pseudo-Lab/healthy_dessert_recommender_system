from typing import List
from gensim.models import Word2Vec
import numpy as np 

class SimilarityUtil:
            
    @staticmethod
    def calc_similarity(query_vector:np.ndarray, candidate_vector:np.ndarray) -> float:
        similarity = np.dot(query_vector, candidate_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(candidate_vector))
        if np.isnan(similarity):
            return 0.0
        return similarity
    
class Word2VecUtil:

    @staticmethod   
    def load_model(model_path):
        try:
            model = Word2Vec.load(model_path)
        except:
            model = Word2Vec()
        return model
    
    @staticmethod
    def get_representation_vector(words:List[str], w2v_model, max_len=50):
        """
        :param:
            words: list of words ; ex) ['word1', 'word2', ...]
            w2v_model: word2vec model
        :return:
            vector: token vector의 평균
        """
        try:
            tokens = [] 
            for word in words:
                if word in w2v_model.wv.key_to_index and len(tokens) < max_len:
                    tokens.append(word)
            return np.mean(w2v_model.wv[tokens], axis=0)
        except:
            return np.zeros(w2v_model.wv.vector_size)

    @staticmethod
    def get_similarity(query: str, candidate: str, model: Word2Vec) -> float:
        """
        :param:
            query: str : query의 description
            candidate: str : candidate의 description
            w2v_model: word2vec model
        :return:
            similarity: float : query와 candidate의 유사도
        """
        query_vector = Word2VecUtil.get_representation_vector(query.split(), model)
        candidate_vector = Word2VecUtil.get_representation_vector(candidate.split(), model)
        return SimilarityUtil.calc_similarity(query_vector, candidate_vector)
