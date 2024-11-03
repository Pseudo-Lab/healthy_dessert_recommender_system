from typing import List, Dict, Any, Optional
from .base import BaseModel
import random

class DefaultModel(BaseModel):

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.code = cfg.get('code', 'default')
        self.version = cfg.get('version', '0.0.0')
        self.topk = cfg.get('topk', 3)  
        
    def fit(self):
        pass

    def predict(self, query_id: int, data: Dict[int, str]) -> Dict[int, float]:
        candidate = list(data.keys())
        candidate.remove(query_id)
        result = {}
        for key in random.sample(candidate, self.topk):
            result[key] = random.random()
        return result

