from typing import List

from pydantic import BaseModel
from app.Models.job import Job
from app.Models.vehicle import Vehicle


class InputModel(BaseModel):
    vehicles: List[Vehicle]
    jobs: List[Job]
    matrix: List[List[int]]

    def getStartingPoints(self) -> List[int]:
        tempList: List[int] = []
        for i in self.vehicles:
            index = i.start_index
            tempList.append(index)
        return tempList

    def getVehicleCapacities(self) -> List[int]:
        return [i.capacity[0] for i in self.vehicles]

    def getCustomersServiceTime(self) -> List[int]:
        temp = [0 for i in range(len(self.matrix))]
        for i in self.jobs:
            temp[i.location_index] += i.service
        return temp

    def getCustomersDemands(self) -> List[int]:
        temp = [0 for i in range(len(self.matrix))]
        for i in self.jobs:
            temp[i.location_index] += i.delivery[0]
        return temp
    # def __init__(self, vehicles: List[Vehicle], jobs: List[Job], matrix: List[List[int]]) -> None:
    #     self.vehicles = vehicles
    #     self.jobs = jobs
    #     self.matrix = matrix
