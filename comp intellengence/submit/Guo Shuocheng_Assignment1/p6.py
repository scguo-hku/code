import sys, parse, grader

def number_of_attacks(problem):
    #Your p6 code here
    current_state = problem
    n = len(current_state)
    
    def calculate_attacks(board):
        attacks = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks
    
    # Generate the attack matrix
    attack_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            temp_board = list(current_state)
            temp_board[j] = i
            attack_matrix[i][j] = calculate_attacks(temp_board)
    
    # Convert the attack matrix to string format, ensuring that each number is two digits
    solution = '\n'.join(' '.join(f'{cell:2}' for cell in row) for row in attack_matrix)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)