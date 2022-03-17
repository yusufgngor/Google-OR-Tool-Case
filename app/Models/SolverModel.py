from typing import List

from app.Models.input_model import InputModel
from app.Models.vehicle import Vehicle


class SolverModel:
    timeMatrix: List[List[int]]

    numberOfLocation: int
    locationDemands: List[int]

    numberOfVehicle: int
    vehicleCapacities: List[int]
    vehicleStartPoints: List[int]
    vehicleEndPoints: List[int]
    vehicles: List[Vehicle]

    @staticmethod
    def setDummies(data: InputModel) -> List[int]:
        # this func set dummy node to give model relaxation for stoping any location
        lastIndexofMatrix = len(data.matrix)
        endPoints = [lastIndexofMatrix for i in range(len(data.vehicles))]
        dummyLocation = [0 for i in range(lastIndexofMatrix)]
        data.matrix.append(dummyLocation)
        for i in data.matrix:
            i.append(0)
        return endPoints

    def __init__(self, input: InputModel):
        # self.inputModel = input
        self.vehicleEndPoints = self.setDummies(input)
        self.timeMatrix = input.matrix
        self.numberOfLocation = len(self.timeMatrix)
        self.locationDemands = input.getCustomersDemands()
        self.numberOfVehicle = len(input.vehicles)
        self.vehicleCapacities = input.getVehicleCapacities()
        self.vehicleStartPoints = input.getStartingPoints()
        self.vehicles = input.vehicles
