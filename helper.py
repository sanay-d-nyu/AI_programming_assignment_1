import math

"""
Here a cluster is a list of vectors (tuple with name, m points for coordinates, 1 numerical value for program A) and state is a list of clusters
"""

# Helper functions for calculating diameter and value of clusters and states
def euclidean_distance(point0, point1, dimension) -> float:
    squares = []
    for i in range(1, dimension + 1):
        squares.append((point1[i] - point0[i]) * (point1[i] - point0[i]))
    return math.sqrt(sum(squares))

def cluster_diameter(cluster, dimension) -> float:
    max_dist = 0
    n = len(cluster)

    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(cluster[i], cluster[j], dimension)
            max_dist = max(max_dist, dist)

    return max_dist

def cluster_value(cluster, dimension) -> float:
    return sum(point[dimension + 1] for point in cluster)

def state_value(state, dimension) -> float:
    state_sum = sum(cluster_value(cluster, dimension) for cluster in state)
    return state_sum

def get_min_vec_state(state) -> str:
    return min(get_min_vec_cluster(cluster) for cluster in state)

def get_min_vec_cluster(cluster) -> str:
    return min(point[0] for point in cluster)

def vec_name_in_state(state, vec_name) -> bool:
    for cluster in state:
        for point in cluster:
            if point[0] == vec_name:
                return True

    return False

def cluster_error(cluster, dimension, tau) -> float:
    return max(0, cluster_diameter(cluster, dimension) - tau)

def state_error(state, dimension, tau) -> float:
    return sum(cluster_error(cluster, dimension, tau) for cluster in state)

# sort clusters in state by name of point for more readable output
def sort_state(state):
    for index, cluster in enumerate(state):
        state[index] = sorted(cluster, key=lambda point: point[0]) #sort by name
