""" Program A 

Solves the problem of "clustering with a diameter threshhold and vector values" (problem 2 from problem set 1)
using iterative deepening
"""

import copy
import helper

def get_successors(state, dimension, omega, max_clusters, tau):
    """Returns the successors of a given state 

    Parameters
    ----------
    state : list
        list of clusters (where a cluster is a list of tuples representing the points in Omega)
    dimension : int
        m, or the dimension of the points in the state space
    omega : list
        the set of all the vectors (points) in the state space
    max_clusters : int
        k, or the maximum number of clusters allowed in a given state
    tau : float
        the maximum diameter of any given cluster

    Returns
    -------
    list of valid successor states, or an empty list if there are no valid successors
    """
    if len(state) == 1 and len(state[0]) == 0:
        return [[[point]] for point in omega]

    min_vec_name = helper.get_min_vec_state(state)
    valid = [
            point 
            for point in omega 
            
            #next line ensures only vectors later in sequence get considered
            if point[0] > min_vec_name and (not helper.vec_name_in_state(state, point[0]))
            ]

    successors = []
    for vec in valid:
        # check if vec can go in any of the clusters
        state_size = len(state)
        for cluster in state:
            cluster_copy = copy.deepcopy(cluster)

            # every cluster must have a unique minimum
            cluster_min_name = helper.get_min_vec_cluster(cluster_copy)
                
            vec_name = vec[0]
            if vec[0] > cluster_min_name:
                # vec can go in this cluster (based on name)
                cluster_copy.append(vec)
                if helper.cluster_diameter(cluster_copy, dimension) <= tau:
                    state_copy = copy.deepcopy(state)

                    for index, copy_clust in enumerate(state_copy):
                        if helper.get_min_vec_cluster(copy_clust) == cluster_min_name:
                            state_copy.pop(index)
                            state_copy.insert(index, copy.deepcopy(cluster_copy))
                            successors.append(state_copy)
                
        #inserting into a cluster didn't work
        if state_size == max_clusters:
            continue

        state_copy = copy.deepcopy(state)
        state_copy.append([vec])
        successors.append(state_copy)


    return successors

def cluster_to_str(cluster):
    """Formats a cluster into a string for printing"""
    ret_list = []
    ret_list.append('{')
    for point in cluster:
        ret_list.append(point[0])
        ret_list.append(',')
    
    ret_list.pop()
    ret_list.append('}')
    return "".join(ret_list)


def state_to_str(state, dimension):
    """Formats a state, along with it's value, into a string for printing"""
    value = helper.state_value(state, dimension)
    ret_list = []
    for cluster in state:
        ret_list.append(cluster_to_str(cluster))
        ret_list.append(',')

    ret_list.pop()
    ret_list.append(' Value={0}'.format(value))
    return ''.join(ret_list)
    
def dfs(state, dimension, omega, max_clusters, tau, goal, curr_depth, max_depth, verbose):
    """Executes DFS on the state space up to a maximum depth of max_depth 

    Parameters
    ----------
    state : list
        list of clusters (where a cluster is a list of tuples representing the points in Omega)
    dimension : int
        m, or the dimension of the points in the state space
    omega : list
        the set of all the vectors (points) in the state space
    max_clusters : int
        k, or the maximum number of clusters allowed in a given state
    tau : float
        the maximum diameter of any given cluster
    goal : int
        T, or the target value for the goal state
    curr_depth : int
        The depth in the state space of the state that dfs is executing only
    max_depth : int
        The maximum allowable depth for this iteration of dfs
    verbose : boolean
        verbose output flag

    Returns
    -------
    The goal state or [[]] (start state or empty state) if a goal state was not found
    """
    if curr_depth != 0:
        if helper.state_value(state, dimension) >= goal:
            return state

    if curr_depth == max_depth:
        return [[]]

    s_states = get_successors(state, dimension, omega, max_clusters, tau)
    for successor in s_states:
        if verbose:         
            print(f"{state_to_str(successor, dimension)}")

        ans = dfs(successor, dimension, omega, max_clusters, tau, goal, curr_depth + 1, max_depth, verbose)
        if len(ans[0]) != 0:
            return ans

    return [[]]

def main():
    dimension = 0
    omega = []
    len_omega = 0
    tau = 0
    max_clusters = 0
    goal = 0
    verbose = False 
    
    # Parse input file
    with open('./input.txt', 'r') as input_file:
        lines_counted = 0
        for index, line in enumerate(input_file):
            stripped = line.strip()
            if len(stripped) == 0:
                continue

            lines_counted += 1
            stripped_split = stripped.split(" ") 

            if lines_counted == 1:
                dimension = int(stripped_split[0])
                len_omega = int(stripped_split[1])
                tau = float(stripped_split[2])
                max_clusters = int(stripped_split[3])
                goal = int(stripped_split[4])
                verbose = True if stripped_split[5] == "V" else False
                continue

            cluster_list_rep = [stripped_split[0]]
            for i in range(1, dimension + 2):
                cluster_list_rep.append(int(stripped_split[i]))

            omega.append(tuple(cluster_list_rep))

            if lines_counted == len_omega + 1:
                break


    # ids implementation
    start_state = [[]]
    for i in range(1, len(omega)):
        if verbose:
            print(f"Depth={i}")

        ans = dfs(start_state, dimension, omega, max_clusters, tau, goal, 0, i, verbose)
        if len(ans[0]) != 0 and helper.state_value(ans, dimension) >= goal:
            print(f"Found solution: {state_to_str(ans, dimension)}")
            return
        if verbose:
            print()

    print("No solution found.")


if __name__ == "__main__":
    main()
