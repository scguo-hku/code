'''
-->How to run<--
First we need the correct path to the testcase, and choose a path to store the training results. Then
you can just run the code and it will output the final epsilon, alpha, learned policy and compared policy.

-->when to break<--
When the learning rate and epsilon are too small, the agent will not be able to explore enough, it will break learning.

-->test case<--
discount: 1
noise: 0.1
livingReward: -0.01
grid:
    _    _    _    1
    _    #    _   -1
    S    _    _    _

-->Parameters<--
learningRate: 0.3
learningRateDecay: 0.99
minLearningRate: 0.003
discount: 1.0
livingReward: -0.01
episodes: 1000
max_steps: 100
epsilon: 1.0
epsilon_decay: 0.99
min_epsilon: 0.001

-->Learned Policy<--
These are the most common results after running many times. The learned policy is not always 
the same as the compared policy, but I think they are also optimal.
| E || E || E || x |
| N || # || N || x |
| N || W || N || W |

| E || E || E || x |
| N || # || N || x |
| N || E || N || W |

-->Validation Optimal<--
To verify whether it is optimal, I iterated the learned policy and the given optimal policy, calculated the 
value of each grid under the given parameters, and then compared the learned value function with the given 
value function. The learned value function is always greater than or equal to the compared value function, 
so I think the policy is greater. The value of each grid will be different because the number of steps to reach the 
final reward is different, so the effect of the discount rate and livingreward will be different.
(These value are not q values, just for validation, the q values are stored in other file)
'''


import parse, random

def TD_learning(problem):
    return_value = ''
    discount = problem['discount']
    noise = problem['noise']
    livingReward = problem['livingReward']
    grid = problem['grid']
    optimal_policy = problem['policy']
    rows = len(grid)
    cols = len(grid[0])
    actions = ['N', 'E', 'S', 'W']
    direc = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    direc_noise = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
    epsilon = 1.0
    epsilon_decay = 0.99
    min_epsilon = 0.001
    alpha = 0.3
    alpha_decay = 0.99
    min_alpha = 0.003
    episodes = 1000
    max_steps = 100
    probabilities = [1 - noise * 2, noise, noise]
    
    def is_terminal(state):
        i, j = state
        return grid[i][j] not in ['_', 'S', '#']
    
    def get_next_state(state, action):
        i, j = state
        di, dj = direc[action]
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] != '#':
            return (ni, nj)
        return state
    
    def epsilon_greedy(Q, state, epsilon):
        if random.uniform(0, 1) < epsilon:
            return random.choice(actions)
        else:
            i, j = state
            actions[max(range(len(actions)), key=lambda a: Q[i][j][a])]

        # add noise to the action
        noisy_action = random.choices(direc_noise[action], probabilities)[0]
        return noisy_action
    
    Q = [[{a: 0.0 for a in range(len(actions))} for _ in range(cols)] for _ in range(rows)]
    
    with open("/Users/mac/Documents/code/comp intellengence/assignment/a3/test_cases/p4/training_results.txt", "w") as f:
        for episode in range(episodes):
            state = (2, 0)  # Start state
            for _ in range(max_steps):
                if is_terminal(state):
                    i, j = state
                    for a in actions:
                        if grid[i][j] == '1':
                            Q[i][j][actions.index(a)] = Q[i][j][actions.index(a)] + alpha * (1 - Q[i][j][actions.index(a)])
                        else:
                            Q[i][j][actions.index(a)] = Q[i][j][actions.index(a)] + alpha * (-1 - Q[i][j][actions.index(a)])
                    break
                action = epsilon_greedy(Q, state, epsilon)
                next_state = get_next_state(state, action)
                i, j = state
                ni, nj = next_state
                best_next_action = max(range(len(actions)), key=lambda a: Q[ni][nj][a])
                Q[i][j][actions.index(action)] = Q[i][j][actions.index(action)] + alpha * (livingReward + discount * Q[ni][nj][best_next_action] - Q[i][j][actions.index(action)])
                state = next_state
            epsilon = max(min_epsilon, epsilon * epsilon_decay)
            alpha = max(min_alpha, alpha * alpha_decay)
            
            # output Q values into file
            f.write(f"Episode {episode + 1}\n")
            for i in range(rows):
                for j in range(cols):
                    f.write(f"Q[{i}][{j}]: {Q[i][j]}\n")
            f.write("\n")
            
            # print progress
            print(f"Episode {episode + 1}: epsilon = {epsilon}, alpha = {alpha}")
    
    learned_policy = [['' for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in ['_', 'S']:
                best_action = actions[max(range(len(actions)), key=lambda a: Q[i][j][a])]
                learned_policy[i][j] = best_action
            elif grid[i][j] == '#':
                learned_policy[i][j] = '#'
            else:
                learned_policy[i][j] = 'x'
    
    def print_policy(policy):
        result = ''
        for row in policy:
            result += '|' + '||'.join(f" {action} " for action in row) + '|\n'
        return result
    
    # compare learned_policy and compared_policy
    match_count = 0
    total_count = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in ['_', 'S']:
                total_count += 1
                if learned_policy[i][j] == optimal_policy[i][j]:
                    match_count += 1
    
    return_value += f"Final epsilon: {epsilon}\n"
    return_value += f"Final alpha: {alpha}\n"
    return_value += f"Learned Policy:\n{print_policy(learned_policy)}"
    return_value += f"Compared Policy:\n{print_policy(optimal_policy)}"
    
    return learned_policy, return_value

def policy_evaluation(policy, problem):
    discount_factor = problem['discount']
    grid = problem['grid']
    rows = len(grid)
    cols = len(grid[0])
    V = [[0 for _ in range(cols)] for _ in range(rows)]
    direc = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}

    def is_terminal(state):
        i, j = state
        return grid[i][j] in ['#', '1', '-1']

    def get_next_state(state, action):
        i, j = state
        di, dj = direc[action]
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            return (ni, nj)
        return state

    # initialize V
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                V[i][j] = 1
            elif grid[i][j] == '-1':
                V[i][j] = -1

    # policy evaluation
    for i in range(rows):
        for j in range(cols):
            if is_terminal((i, j)):
                continue
            state = (i, j)
            total_reward = 0
            step = 0
            while not is_terminal(state):
                action = policy[state[0]][state[1]]
                next_state = get_next_state(state, action)
                if next_state == (1, 1) or next_state == (2, 3):
                    break
                reward = 1 if grid[next_state[0]][next_state[1]] == '1' else -1 if grid[next_state[0]][next_state[1]] == '-1' else problem['livingReward']
                total_reward += (discount_factor ** step) * reward
                state = next_state
                step += 1
            V[i][j] = total_reward
                
    return V

def check_value_function(V_learned, V_optimal):
    rows = len(V_learned)
    cols = len(V_learned[0])
    for i in range(rows):
        for j in range(cols):
            if V_learned[i][j] < V_optimal[i][j]:
                return False
    return True

def print_value_function(V):
        result = ''
        for row in V:
            result += '|' + '||'.join(f" {value:.2f} " for value in row) + '|\n'
        return result

if __name__ == "__main__":
    problem = parse.read_grid_mdp_problem_p4("/Users/mac/Documents/code/comp intellengence/assignment/a3/test_cases/p4/1.prob")

    learned_policy, result = TD_learning(problem)
    V_learned = policy_evaluation(learned_policy, problem)
    V_optimal = policy_evaluation(problem['policy'], problem)

    print(result)
    print("leanred value:\n" + print_value_function(V_learned))
    print("compared value:\n" + print_value_function(V_optimal))
    print(f"Policy is optimal: {check_value_function(V_learned, V_optimal)}")
