import sys, parse, grader

def better_board(problem):
    #Your p7 code here
    current_state = problem
    n = len(current_state)
    
    def calculate_attacks(board):
        attacks = 0
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                    attacks += 1
        return attacks
    
    # find the best state
    best_state = list(current_state)
    min_attacks = calculate_attacks(current_state)
    
    for col in range(n):
        for row in range(n):
            if current_state[col] != row:
                temp_state = list(current_state)
                temp_state[col] = row
                attacks = calculate_attacks(temp_state)
                if attacks < min_attacks:
                    min_attacks = attacks
                    best_state = list(temp_state)
    
    # Generate a new board state
    new_board = [['.'] * n for _ in range(n)]
    for col in range(n):
        new_board[best_state[col]][col] = 'q'
    
    # Convert the new board state to string format
    solution = '\n'.join(' '.join(row) for row in new_board)
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)