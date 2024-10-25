from pydantic import BaseModel
from typing import List

class BbangleSimRequest(BaseModel):
    member_id : int

class BbangleSimResponse(BaseModel):
    class Recommendation(BaseModel):
        section_id : int
        class Model(BaseModel):
            mo1del_id : str
        class Item(BaseModel):
            product_board_id : int
            score : float
        items : List[Item]
    results : List[Recommendation]

class BbangleSimResponse(BaseModel):
    class Recommendation(BaseModel):
        class Model(BaseModel):
            id : int
        class Item(BaseModel):
            section_id : int
            product_board_id : int
            score : float
        items : List[Item]
    results : List[Recommendation]




request = {
    "member_id" : 1
}

response ={
    "results" : [ 
        {
            "model" : {"id": 1},
            "items" : [
                {
                    "section_id" : 1,
                    "product_board_id" : 1,
                    "score" : 0.9
                },
                {
                    "section_id" : 2,
                    "product_board_id" : 2,
                    "score" : 0.8
                },
                {
                    "section_id" : 3,
                    "product_board_id" : 3,
                    "score" : 0.7
                }
            ]
        }
    ]
}


results = {
    "results": [
        {
            "section_id" : 1,
            "model" : {
                "model_id" : "sim_model_1"
            },
            "items" : [
                {
                    "product_board_id" : 1,
                    "score" : 0.9
                }
            ]
        },
        {
            "section_id" : 2,
            "model" : {
                "model_id" : "sim_model_1"
            },
            "items" : [
                {
                    "product_board_id" : 2,
                    "score" : 0.8
                }
            ]
        },
        {
            "section_id" : 3,
            "model" : {
                "model_id" : "sim_model_1"
            },
            "items" : [
                {
                    "product_board_id" : 3,
                    "score" : 0.7
                }
            ]
        }
    ]
}

if __name__ == "__main__":
    # request_dto = BbangleSimRequestDTO.model_validate(request)
    # print(request_dto)
    response_dto = BbangleSimResponse.model_validate(response)
    print(response_dto)

