'''
-->How to run<--
First we need the correct path to the testcase, and choose a path to store the training results. Then
you can just run the code and it will output the final epsilon, alpha, learned policy and compared policy.

-->Parameters<--
learningRate: 0.3
learningRateDecay: 0.99
minLearningRate: 0.003
discount: 0.9
livingReward: -0.04
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
| E || E || N || W |

| E || E || E || x |
| N || # || N || x |
| N || E || N || W |
'''

import parse, random

def TD_learning(problem):
    return_value = ''
    discount = problem['discount']
    livingReward = problem['livingReward']
    grid = problem['grid']
    optimal_policy = problem['policy']
    rows = len(grid)
    cols = len(grid[0])
    actions = ['N', 'E', 'S', 'W']
    direc = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    epsilon = 1.0
    epsilon_decay = 0.99
    min_epsilon = 0.001
    alpha = 0.3
    alpha_decay = 0.99
    min_alpha = 0.003
    episodes = 1000
    max_steps = 100
    
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
            return actions[max(range(len(actions)), key=lambda a: Q[i][j][a])]
    
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
    
    return return_value

if __name__ == "__main__":
    problem = parse.read_grid_mdp_problem_p4("/Users/mac/Documents/code/comp intellengence/assignment/a3/test_cases/p4/1.prob")
    print(TD_learning(problem))