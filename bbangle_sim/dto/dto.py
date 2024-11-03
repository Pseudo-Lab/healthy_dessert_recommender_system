from pydantic import BaseModel
from typing import List

class BbangleSimRequest(BaseModel):
    member_id : int
    query_item : int

class BbangleSimResponse(BaseModel):
    class Recommendation(BaseModel):
        theme : str
        class Model(BaseModel):
            model_version : str
        class Item(BaseModel):
            product_board_id : int
            score : float
            rank : int
        items : List[Item]
    results : List[Recommendation]

mock_request = BbangleSimRequest(
    member_id=12345,
    query_item=67890
)

# Mock-up response data
mock_response = BbangleSimResponse(
    results=[
        BbangleSimResponse.Recommendation(
            theme= 'similarity',
            model=BbangleSimResponse.Recommendation.Model(
                model_version="v1.0"
            ),
            items=[
                BbangleSimResponse.Recommendation.Item(
                    product_board_id=1111,
                    score=0.95,
                    rank=1
                ),
                BbangleSimResponse.Recommendation.Item(
                    product_board_id=2222,
                    score=0.89,
                    rank=2
                ),
                BbangleSimResponse.Recommendation.Item(
                    product_board_id=3333,
                    score=0.87,
                    rank=3
                )
            ]
        ),
        BbangleSimResponse.Recommendation(
            theme='similarity',
            model=BbangleSimResponse.Recommendation.Model(
                model_version="v1.0"
            ),
            items=[
                BbangleSimResponse.Recommendation.Item(
                    product_board_id=4444,
                    score=0.91,
                    rank=1
                ),
                BbangleSimResponse.Recommendation.Item(
                    product_board_id=5555,
                    score=0.88,
                    rank=2
                ),
                BbangleSimResponse.Recommendation.Item(
                    product_board_id=5555,
                    score=0.70,
                    rank=3
                )
            ]
        )
    ]
)

# 출력 확인
print(mock_request)
print(mock_response)

if __name__ == "__main__":
    # request_dto = BbangleSimRequestDTO.model_validate(request)
    # print(request_dto)
    response_dto = BbangleSimResponse.model_validate(mock_response)
    print(mock_response)

