"""Helper functions for calculating diameter and value of clusters and states

Here a cluster is a list of vectors (tuple with name, m points for coordinates, 1 numerical value for program A) and state is a list of clusters
"""

import math

def euclidean_distance(point0, point1, dimension) -> float:
    """Returns the euclidean distance between two points given the dimension of those points"""
    squares = []
    for i in range(1, dimension + 1):
        squares.append((point1[i] - point0[i]) * (point1[i] - point0[i]))
    return math.sqrt(sum(squares))

def cluster_diameter(cluster, dimension) -> float:
    """Returns the diameter of a cluster given the dimension of the points in that cluster"""
    max_dist = 0
    n = len(cluster)

    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(cluster[i], cluster[j], dimension)
            max_dist = max(max_dist, dist)

    return max_dist

def cluster_value(cluster, dimension) -> float:
    """Returns the value of a cluster by summing the values of all it's points"""
    return sum(point[dimension + 1] for point in cluster)

def state_value(state, dimension) -> float:
    """Returns the value of a state by summing the values of all it's clusters"""
    state_sum = sum(cluster_value(cluster, dimension) for cluster in state)
    return state_sum

def get_min_vec_state(state) -> str:
    """Returns the lexicographic minimum of all the points in a given state

    Example:
        state = [[('a', 0, 0, 1), ('b', 1, 1, 1)]]
        min_name = get_min_vec_state(state) # min_name = 'a'
    """
    return min(get_min_vec_cluster(cluster) for cluster in state)

def get_min_vec_cluster(cluster) -> str:
    """Returns the lexicographic minimum of all the points in a given cluster

    Example:
        cluster = [('a', 0, 0, 1), ('b', 1, 1, 1)]
        min_name = get_min_vec_cluster(cluster) # min_name = 'a'
    """
    return min(point[0] for point in cluster)

def vec_name_in_state(state, vec_name) -> bool:
    """Checks if the given state has a point with the same name as the given vec_name"""
    for cluster in state:
        for point in cluster:
            if point[0] == vec_name:
                return True

    return False

def cluster_error(cluster, dimension, tau) -> float:
    """Returns the error of the cluster, given the diameter and tau"""
    return max(0, cluster_diameter(cluster, dimension) - tau)

def state_error(state, dimension, tau) -> float:
    """Returns the error of the state, given the diameter and tau, by summing the errors of all it's clusters"""
    return sum(cluster_error(cluster, dimension, tau) for cluster in state)

def sort_state(state):
    """Sorts the state by the names of it's points"""
    for index, cluster in enumerate(state):
        state[index] = sorted(cluster, key=lambda point: point[0]) #sort by name
