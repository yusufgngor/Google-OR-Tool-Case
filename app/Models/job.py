from typing import List
from pydantic import BaseModel


class Job(BaseModel):
    id: int
    location_index: int
    delivery: List[int]
    service: int

    # def __init__(self, id: int, location_index: int, delivery: List[int], service: int) -> None:
    #     self.id = id
    #     self.location_index = location_index
    #     self.delivery = delivery
    #     self.service = service