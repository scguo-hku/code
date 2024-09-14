import os, sys
def read_graph_search_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Extract the start state
    start_state = lines[0].strip().split(": ")[1]
    
    # Extract the goal state
    goal_states = lines[1].strip().split(": ")[1]
    
    # Extract the heuristics value
    heuristics = {}
    i = 2
    while i < len(lines) and len(lines[i].strip().split()) == 2:
        state, heuristic = lines[i].strip().split()
        heuristics[state] = float(heuristic)
        i += 1
    
    # Extract the transitions value
    transitions = {}
    while i < len(lines):
        start, end, cost = lines[i].strip().split()
        if start not in transitions:
            transitions[start] = []
        transitions[start].append((float(cost), end))
        i += 1
    
    problem = {
        'start_state': start_state,
        'goal_states': goal_states,
        'heuristics': heuristics,
        'transitions': transitions
    }
    
    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    board = []
    for line in lines:
        row = []
        for char in line.strip().split():
            if char == 'q':
                row.append(1)
            else:
                row.append(0)
        board.append(row)
    
    # Convert the board state to a format suitable for local search algorithms
    n = len(board)
    problem = [-1] * n
    for row_index in range(n):
        for col_index in range(n):
            if board[row_index][col_index] == 1:
                problem[col_index] = row_index
    
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')