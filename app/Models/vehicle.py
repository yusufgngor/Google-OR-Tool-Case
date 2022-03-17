from typing import List

from pydantic import BaseModel


class Vehicle(BaseModel):
    id: int
    start_index: int
    capacity: List[int]

    # def __init__(self, id: int, start_index: int, capacity: List[int]) -> None:
    #     self.id = id
    #     self.start_index = start_index
    #     self.capacity = capacity
