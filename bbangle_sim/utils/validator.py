from typing import Dict

class RecommendationValidator:
    @staticmethod
    def valid_topk(result: Dict[int, float], topk: int):
        if len(result) < topk:
            raise ValueError("Invalid topk result")