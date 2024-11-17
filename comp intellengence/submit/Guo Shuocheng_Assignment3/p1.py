import sys, grader, parse, random

def play_episode(problem):
    experience = ''
    seed = problem['seed']
    noise = problem['noise']
    livingReward = problem['livingReward']
    grid = problem['grid']
    policy = problem['policy']
    direc = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']} 

    if seed != -1:
        random.seed(seed, version=1)
    
    # find start position
    start_pos = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                start_pos = (i, j)
                break
        if start_pos:
            break
    
    # initialize variables
    current_pos = start_pos
    cumulative_reward = 0.0
    grid[current_pos[0]][current_pos[1]] = 'P'
    
    def print_grid(grid):
        grid_str = ''
        for row in grid:
            grid_str += ''.join(f"{cell:>5}" for cell in row) + '\n'
        return grid_str
    
    def format_number(num):
        if isinstance(num, float):
            formatted = f"{num:.10g}"  # use scientific notation if too long
            if '.' not in formatted:
                formatted = f"{num:.1f}"  # show one decimal place
            return formatted
        return str(num)
    
    experience += "Start state:\n"
    experience += print_grid(grid)
    experience += f"Cumulative reward sum: {format_number(cumulative_reward)}\n"
    experience += "-------------------------------------------- \n"
    
    while True:
        i, j = current_pos
        intended_action = policy[i][j]
        possible_actions = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
        
        # according noise, choose the action
        action = random.choices(
            population=direc[intended_action],
            weights=[1 - noise * 2, noise, noise]
        )[0]
        
        di, dj = possible_actions[action]
        new_pos = (i + di, j + dj)
        
        # check if the new position is valid
        if (0 <= new_pos[0] < len(grid) and
            0 <= new_pos[1] < len(grid[0]) and
            grid[new_pos[0]][new_pos[1]] != '#'):
            current_pos = new_pos
        
        # update reward
        reward = livingReward
        if policy[current_pos[0]][current_pos[1]] == 'exit':
            exit_num = float(grid[current_pos[0]][current_pos[1]])
            cumulative_reward += reward
            experience += f"Taking action: {action} (intended: {intended_action})\n"
            experience += f"Reward received: {reward}\n"
            experience += "New state:\n"
            grid[i][j] = 'S' if (i, j) == start_pos else '_'
            grid[current_pos[0]][current_pos[1]] = 'P'
            experience += print_grid(grid)
            experience += f"Cumulative reward sum: {format_number(cumulative_reward)}\n"
            experience += "-------------------------------------------- \n"
            experience += f"Taking action: exit (intended: exit)\n"
            experience += f"Reward received: {format_number(exit_num)}\n"
            experience += "New state:\n"
            grid[current_pos[0]][current_pos[1]] = int(exit_num)
            cumulative_reward += exit_num
            experience += print_grid(grid)
            experience += f"Cumulative reward sum: {format_number(cumulative_reward)}"
            break
        
        cumulative_reward += reward
        
        # update grid
        grid[i][j] = 'S' if (i, j) == start_pos else '_'
        grid[current_pos[0]][current_pos[1]] = 'P'
        
        experience += f"Taking action: {action} (intended: {intended_action})\n"
        experience += f"Reward received: {format_number(reward)}\n"
        experience += "New state:\n"
        experience += print_grid(grid)
        experience += f"Cumulative reward sum: {format_number(cumulative_reward)}\n"
        experience += "-------------------------------------------- \n"
    
    return experience

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)