import copy
import helper
import random

def cluster_to_str(cluster):
    ret_list = []
    ret_list.append('{')
    for point in cluster:
        ret_list.append(point[0])
        ret_list.append(',')
    
    ret_list.pop()
    ret_list.append('}')
    return "".join(ret_list)


def state_to_str(state, dimension, tau):
    ret_list = []
    for cluster in state:
        ret_list.append(cluster_to_str(cluster))
        ret_list.append(',')

    ret_list.pop()
    ret_list.append(' Error={0:.4f}'.format(helper.state_error(state, dimension, tau)))
    return ''.join(ret_list)

# generates a random state according to the method specified in the assignment
def random_state(omega, max_clusters):
    omega_copy = copy.deepcopy(omega)
    ret_state = []
    for i in range(max_clusters):
        chosen_index = random.randint(0, len(omega_copy) - 1)
        ret_state.append([omega_copy[chosen_index]])
        omega_copy.pop(chosen_index)

    for i in range(len(omega_copy)):
        chosen_cluster_index = random.randint(0, max_clusters - 1)
        ret_state[chosen_cluster_index].append(omega_copy[-1])
        omega_copy.pop()
    
    helper.sort_state(ret_state)
    return ret_state


def get_neighbors(state):
    neighbors = []
    for i, cluster in enumerate(state):
        if not len(cluster) >= 2:
            continue

        for j, point in enumerate(cluster):
            for k, inner_cluster in enumerate(state):
                if k == i:
                    continue
                state_copy = copy.deepcopy(state)
                cluster_copy = copy.deepcopy(cluster)
                cluster_copy.pop(j)
                inner_cluster_copy = copy.deepcopy(inner_cluster)
                inner_cluster_copy.append(point)
                state_copy.pop(i)
                state_copy.insert(i, copy.deepcopy(cluster_copy))
                state_copy.pop(k)
                state_copy.insert(k, copy.deepcopy(inner_cluster_copy))
                helper.sort_state(state_copy)
                neighbors.append(state_copy)

    return neighbors

def hill_climbing(state, dimension, tau, verbose):
    neighbors = get_neighbors(state)
    min_error = helper.state_error(state, dimension, tau)
    min_index = -1

    if verbose:
        print('Neighbors:')

    for index, neighbor in enumerate(neighbors):
        if verbose:
            print(f'{state_to_str(neighbor, dimension, tau)}')

        neighbor_error = helper.state_error(neighbor, dimension, tau)
        if neighbor_error == 0:
            return neighbor

        if neighbor_error < min_error:
            min_error = neighbor_error
            min_index = index
    
    if verbose:
        print()

    if min_index == -1:
        if verbose:
            print('Search failed')
            print()
        return None
    
    if verbose:
        print('Move to')
        print(f'{state_to_str(neighbors[min_index], dimension, tau)}')
        print()

    return hill_climbing(neighbors[min_index], dimension, tau, verbose) # call hill climb on best neighbor
     


def main():
    dimension = 0
    omega = []
    len_omega = 0
    tau = 0
    max_clusters = 0
    max_restarts = 0
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
                max_restarts = int(stripped_split[4])
                verbose = True if stripped_split[5] == "V" else False
                continue

            cluster_list_rep = [stripped_split[0]]
            for i in range(1, dimension + 1):
                cluster_list_rep.append(int(stripped_split[i]))

            omega.append(tuple(cluster_list_rep))

            if lines_counted == len_omega + 1:
                break
    
    #implementation of hill climbing with random restarts
    restarts = 0
    while restarts < max_restarts:
        start_state = random_state(omega, max_clusters)
        helper.sort_state(start_state)
        if verbose:
            print(f'Randomly chosen start state:')
            print(f'{state_to_str(start_state, dimension, tau)}')

        hill_result = hill_climbing(start_state, dimension, tau, verbose)
        if hill_result != None:
            print(f'Found solution: {state_to_str(hill_result, dimension, tau)}')
            return

        restarts += 1

    print('No solution found.')


if __name__ == "__main__":
    main()
