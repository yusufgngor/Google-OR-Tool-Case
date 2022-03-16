from unittest import result
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from Models.SolverModel import SolverModel

from Models.input_model import InputModel
from Models.result import Result


def print_solution(data: SolverModel, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0

    for vehicle_id in range(data.numberOfVehicle):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data.locationDemands[node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    return 0, 0


def solver(data: SolverModel) -> Result | str:

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(data.numberOfLocation,
                                           data.numberOfVehicle, data.vehicleStartPoints, data.vehicleEndPoints)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data.timeMatrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        86400,  # vehicle maximum travel time -> a day
        True,  # start cumul to zero
        "time")

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data.locationDemands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        data.vehicleCapacities,
        True,
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
        result = Result._getResultFromSolverSolution(
            data, manager, routing, solution)
        return result
    else:
        return'No solution found !'
