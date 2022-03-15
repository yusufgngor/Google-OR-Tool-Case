"""Simple Vehicles Routing Problem."""

from asyncio.windows_events import NULL
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from Models.input_model import InputModel


def print_solution(data: InputModel, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0

    for vehicle_id in range(len(data.vehicles)):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data.getCustomersDemands()[node_index]
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


def solver(data: InputModel):
    """Entry point of the program."""
    lastIndex = len(data.matrix[0])
    dummyVehiclePoint = [lastIndex for i in range(len(data.vehicles))]
    dummyLocation = [0 for i in range(lastIndex)]
    data.matrix.append(dummyLocation)
    for i in data.matrix:
        i.append(0)

    print(data.getVehicleCapacities())
    print(data.getCustomersDemands())

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data.matrix),
                                           len(data.vehicles), data.getStartingPoints(),  dummyVehiclePoint)

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)
    # Create and register a transit callback.

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data.matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'time'
    routing.AddDimension(
        evaluator_index=transit_callback_index,
        slack_max=250000,
        fix_start_cumul_to_zero=True,
        name=dimension_name,
        capacity=200000
    )

    # distance_dimension = routing.GetDimensionOrDie(dimension_name)
    # distance_dimension.SetGlobalSpanCostCoefficient(1)

    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data.getCustomersDemands()[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data.getVehicleCapacities(),  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)


    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        plan_output, max_route_distance = print_solution(
            data, manager, routing, solution)
        return plan_output, max_route_distance
    else:
        return'No solution found !', NULL
