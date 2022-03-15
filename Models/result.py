from typing import List, Dict

from Models.SolverModel import SolverModel
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from Models.job import Job


class Routes:
    jobs: List[int]
    delivery_duration: int

    def __init__(self, jobs: List[int], delivery_duration: int = 0) -> None:
        self.jobs = jobs
        self.delivery_duration = delivery_duration


class Result:
    total_delivery_duration: int
    routes: Dict[str, Routes]

    def __init__(self, total_delivery_duration: int, routes: Dict[str, Routes]) -> None:
        self.total_delivery_duration = total_delivery_duration
        self.routes = routes

    @staticmethod
    def _getResultFromSolverSolution(data: SolverModel, manager: pywrapcp.RoutingIndexManager, routing: pywrapcp.RoutingModel, solution: pywrapcp.Assignment):
        total_distance = 0
        total_load = 0
        routes: Dict[str, int] = {}
        for vehicle_id in range(data.numberOfVehicle):
            index = routing.Start(vehicle_id)
            realVID = data.vehicles[vehicle_id]
            route_distance = 0
            route_load = 0
            jobs = []
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data.locationDemands[node_index]
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                jobs.append(manager.IndexToNode(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            jobs.pop()
            routes[realVID.id] = Routes(
                jobs=jobs, delivery_duration=route_distance)
            total_distance += route_distance
            total_load += route_load
        return Result(routes=routes, total_delivery_duration=total_distance)
