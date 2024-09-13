import os, sys
def read_graph_search_problem(file_path):
    #Your p1 code here
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 提取起始状态
    start_state = lines[0].strip().split(": ")[1]
    
    # 提取目标状态列表
    goal_states = lines[1].strip().split(": ")[1]
    
    # 提取启发式值
    heuristics = {}
    i = 2
    while i < len(lines) and len(lines[i].strip().split()) == 2:
        state, heuristic = lines[i].strip().split()
        heuristics[state] = float(heuristic)
        i += 1
    
    # 提取状态转换信息
    transitions = {}
    while i < len(lines):
        start, end, cost = lines[i].strip().split()
        if start not in transitions:
            transitions[start] = []
        transitions[start].append((float(cost), end))
        i += 1
    
    # 返回搜索问题的内容
    problem = {
        'start_state': start_state,
        'goal_states': goal_states,
        'heuristics': heuristics,
        'transitions': transitions
    }
    
    return problem

def read_8queens_search_problem(file_path):
    #Your p6 code here
    problem = ''
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