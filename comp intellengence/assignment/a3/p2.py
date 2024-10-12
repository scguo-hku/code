import sys, grader, parse

def policy_evaluation(problem):
    return_value = ''
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    iterations = problem['iterations']
    grid = problem['grid']
    policy = problem['policy']
    direc = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']} 
    probabilities = [1 - noise * 2, noise, noise]
    
    rows = len(grid)
    cols = len(grid[0])
    V = [[0.0 if grid[i][j] != '#' else '#' for j in range(cols)] for i in range(rows)]
    
    def print_values(V, k, last_interation=False):
        """
        Print the value function V for iteration k in the specified format.
        """
        result = f"V^pi_k={k}\n"
        for i, row in enumerate(V):
            result += '|' + '||'.join(f"{value:7.2f}" if value != '#' else ' ##### ' for value in row)
            if i < len(V) - 1 or not last_interation:
                result += '|\n'
            else:
                result += '|'
        return result
    
    # Print initial state (all zeros)
    return_value += print_values(V, 0)
    
    # Initialize V with initial values from the grid
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] not in ['_', 'S']:
                V[i][j] = float(grid[i][j]) if grid[i][j] != '#' else '#'
            else:
                V[i][j] = livingReward
    
    # Print initial value function
    return_value += print_values(V, 1)
    
    # Iterate for the specified number of iterations
    for k in range(2, iterations):
        new_V = [[0.0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] not in ['_', 'S']:
                    new_V[i][j] = float(grid[i][j]) if grid[i][j] != '#' else '#'
                else:
                    action = policy[i][j]
                    value_sum = 0.0
                    for prob, direction in zip(probabilities, direc[action]):
                        if direction == 'N':
                            ni, nj = i - 1, j
                        elif direction == 'E':
                            ni, nj = i, j + 1
                        elif direction == 'S':
                            ni, nj = i + 1, j
                        elif direction == 'W':
                            ni, nj = i, j - 1
                        
                        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] != '#':
                            reward = livingReward
                            if grid[ni][nj] not in ['_', 'S']:
                                reward += float(grid[ni][nj])
                            value_sum += prob * (livingReward + discount * V[ni][nj])
                        else:
                            value_sum += prob * (livingReward + discount * V[i][j])
                    new_V[i][j] = value_sum
        V = new_V
        return_value += print_values(V, k, last_interation=(k == iterations - 1))
    
    return return_value

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)