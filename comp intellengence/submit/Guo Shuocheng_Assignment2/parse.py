import os, sys
def read_layout_problem(file_path):
    #Your p1 code here
    problem = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        problem['seed'] = lines[0].strip().split(': ')[1]  # get seed value
        problem['layout'] = ''.join(lines[1:]).strip()  # get layout
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')