import os, sys

def read_grid_mdp_problem_p1(file_path):
    #Your p1 code here
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # read seed, noise, livingReward
        for line in lines:
            if line.startswith('seed'):
                problem['seed'] = int(line.split(':')[1].strip())
            elif line.startswith('noise'):
                problem['noise'] = float(line.split(':')[1].strip())
            elif line.startswith('livingReward'):
                problem['livingReward'] = float(line.split(':')[1].strip())
            elif line.startswith('grid'):
                break
        
        # read grid
        grid = []
        grid_start = lines.index('grid:\n') + 1
        for line in lines[grid_start:]:
            if line.startswith('policy'):
                break
            grid.append(line.strip().split())
        problem['grid'] = grid
        
        # read policy
        policy = []
        policy_start = lines.index('policy:\n') + 1
        for line in lines[policy_start:]:
            policy.append(line.strip().split())
        problem['policy'] = policy
    
    return problem

def read_grid_mdp_problem_p2(file_path):
    #Your p2 code here
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        # read seed, noise, livingReward
        for line in lines:
            if line.startswith('discount'):
                problem['discount'] = float(line.split(':')[1].strip())
            elif line.startswith('noise'):
                problem['noise'] = float(line.split(':')[1].strip())
            elif line.startswith('livingReward'):
                problem['livingReward'] = float(line.split(':')[1].strip())
            elif line.startswith('iterations'):
                problem['iterations'] = int(line.split(':')[1].strip())
            elif line.startswith('grid'):
                break
        
        # read grid
        grid = []
        grid_start = lines.index('grid:\n') + 1
        for line in lines[grid_start:]:
            if line.startswith('policy'):
                break
            grid.append(line.strip().split())
        problem['grid'] = grid
        
        # read policy
        policy = []
        policy_start = lines.index('policy:\n') + 1
        for line in lines[policy_start:]:
            policy.append(line.strip().split())
        problem['policy'] = policy
    
    return problem

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = ''
    return problem


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_grid_mdp_problem_p2(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')