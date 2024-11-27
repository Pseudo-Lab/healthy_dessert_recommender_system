from collections import defaultdict
from utils.validator import RecommendationValidator
from typing import Dict, Union
class RecommendationGenerator:

    def __init__(self, service_cfg, target_model, default_model):
        self.service_cfg = service_cfg
        self.target_model = target_model
        self.default_model = default_model
        
    def generate(self, data:Dict[int, str]) -> Dict[int, Dict[str, Union[Dict, str]]]:
        rec_result = defaultdict()
        for key in data.keys():
            query_id = key
            try:
                model = self.target_model
                items = model.predict(query_id, data)
                RecommendationValidator.valid_topk(items, self.service_cfg['service']['topk'])
            except Exception as e:
                model = self.default_model 
                items = model.predict(query_id, data)
            finally:
                rec_result[query_id]  = {'items': items, 'recommendation_theme': model.code, 'model_version': model.version}
        return rec_result


