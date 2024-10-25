from typing import List


def get_coverage(impression_items: List[int], total_cnt: int) -> float:
    """
    :params:
        impression_items : List[int] : recommendation set
        total_cnt : int : total count of items
    :return:
        coverage : float : coverage rate
    """ 
    rec_set = set(impression_items)
    return len(rec_set) / total_cnt