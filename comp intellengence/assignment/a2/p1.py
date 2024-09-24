import sys, random, grader, parse
EAT_FOOD_SCORE = 10 
PACMAN_EATEN_SCORE = -500 
PACMAN_WIN_SCORE = 500 
PACMAN_MOVING_SCORE = -1 

def random_play_single_ghost(problem):
    #Your p1 code here
    seednum = problem['seed']
    layout = problem['layout'].split('\n')

    def move(layout):
        n = len(layout)
        m = len(layout[0])
        
        # find Pacman and Ghost position
        pacman_pos = None
        ghost_pos = None
        for i in range(n):
            for j in range(m):
                if layout[i][j] == 'P':
                    pacman_pos = (i, j)
                elif layout[i][j] == 'W':
                    ghost_pos = (i, j)
        
        # find Pacman move directions
        pacman_moves = []
        if pacman_pos:
            i, j = pacman_pos
            if i > 0 and layout[i-1][j] != '%':  # North
                pacman_moves.append('N')
            if i < n-1 and layout[i+1][j] != '%':  # South
                pacman_moves.append('S')
            if j > 0 and layout[i][j-1] != '%':  # West
                pacman_moves.append('W')
            if j < m-1 and layout[i][j+1] != '%':  # East
                pacman_moves.append('E')
        
        # find Ghost move directions
        ghost_moves = []
        if ghost_pos:
            i, j = ghost_pos
            if i > 0 and layout[i-1][j] != '%':  # North
                ghost_moves.append('N')
            if i < n-1 and layout[i+1][j] != '%':  # South
                ghost_moves.append('S')
            if j > 0 and layout[i][j-1] != '%':  # West
                ghost_moves.append('W')
            if j < m-1 and layout[i][j+1] != '%':  # East
                ghost_moves.append('E')
        
        # sort by the alphabet order
        pacman_moves.sort()
        ghost_moves.sort()
        
        # output Pacman and Ghost directions
        direction = {
            'pacman': pacman_moves,
            'ghost': ghost_moves
        }

        return direction

    random.seed(int(seednum), version=1)
    
    # find Pacman and Ghost position
    pacman_pos = None
    ghost_pos = None
    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if layout[i][j] == 'P':
                pacman_pos = (i, j)
            elif layout[i][j] == 'W':
                ghost_pos = (i, j)
    
    score = 0
    game_over = False
    round_num = 0
    next_char = ' '
    
    # Output initial seed value and layout
    solution = []
    solution.append(f'seed: {seednum}')
    solution.append(str(round_num))
    for row in layout:
        solution.append(row)
    
    while not game_over:
        # input()
        round_num += 1
        
        # Get Pacman and Ghost move directions
        direction = move(layout)
        
        # Pacman move
        if direction['pacman']:
            pacman_move = random.choice(direction['pacman'])
            new_pacman_pos = {
                'N': (pacman_pos[0] - 1, pacman_pos[1]),
                'S': (pacman_pos[0] + 1, pacman_pos[1]),
                'W': (pacman_pos[0], pacman_pos[1] - 1),
                'E': (pacman_pos[0], pacman_pos[1] + 1)
            }[pacman_move]
            
            # Update layout and score
            if layout[new_pacman_pos[0]][new_pacman_pos[1]] == '.':
                score += EAT_FOOD_SCORE
                layout[new_pacman_pos[0]] = layout[new_pacman_pos[0]][:new_pacman_pos[1]] + ' ' + layout[new_pacman_pos[0]][new_pacman_pos[1]+1:]
            score += PACMAN_MOVING_SCORE
            
            # update layout and Pacman position
            layout[pacman_pos[0]] = layout[pacman_pos[0]][:pacman_pos[1]] + ' ' + layout[pacman_pos[0]][pacman_pos[1]+1:]
            layout[new_pacman_pos[0]] = layout[new_pacman_pos[0]][:new_pacman_pos[1]] + 'P' + layout[new_pacman_pos[0]][new_pacman_pos[1]+1:]
            pacman_pos = new_pacman_pos
            
            # Check if Ghost catches Pacman
            if ghost_pos == pacman_pos:
                score += PACMAN_EATEN_SCORE
                game_over = True
                layout[pacman_pos[0]] = layout[pacman_pos[0]][:pacman_pos[1]] + 'W' + layout[pacman_pos[0]][pacman_pos[1]+1:]
                solution.append(f'{round_num}: P moving {pacman_move}')
                for row in layout:
                    solution.append(row)
                solution.append(f'score: {score}')
                solution.append('WIN: Ghost')
                break

            # Output Pacman move layout and score
            solution.append(f'{round_num}: P moving {pacman_move}')
            round_num += 1
            
            for row in layout:
                solution.append(row)
                
            # Check if Pacman wins
            if all('.' not in row for row in layout):
                score += PACMAN_WIN_SCORE
                game_over = True
                solution.append(f'score: {score}')
                solution.append('WIN: Pacman')
                break
            solution.append(f'score: {score}')
            
            
        # Ghost move
        if not game_over and direction['ghost']:
            ghost_move = random.choice(direction['ghost'])
            new_ghost_pos = {
                'N': (ghost_pos[0] - 1, ghost_pos[1]),
                'S': (ghost_pos[0] + 1, ghost_pos[1]),
                'W': (ghost_pos[0], ghost_pos[1] - 1),
                'E': (ghost_pos[0], ghost_pos[1] + 1)
            }[ghost_move]

            if (round_num == 1):
                continue
            else:
                # Restore the position with food when the ghost leaves
                if next_char == '.':
                    layout[ghost_pos[0]] = layout[ghost_pos[0]][:ghost_pos[1]] + '.' + layout[ghost_pos[0]][ghost_pos[1]+1:]
                else:
                    layout[ghost_pos[0]] = layout[ghost_pos[0]][:ghost_pos[1]] + ' ' + layout[ghost_pos[0]][ghost_pos[1]+1:]
                
            # Save the character at the new position where the Ghost is about to move
            next_char = layout[new_ghost_pos[0]][new_ghost_pos[1]]

            # update Ghost position
            layout[new_ghost_pos[0]] = layout[new_ghost_pos[0]][:new_ghost_pos[1]] + 'W' + layout[new_ghost_pos[0]][new_ghost_pos[1]+1:]
            ghost_pos = new_ghost_pos

            # Check if Ghost catches Pacman
            if ghost_pos == pacman_pos:
                score += PACMAN_EATEN_SCORE
                game_over = True
                solution.append(f'{round_num}: W moving {ghost_move}')
                for row in layout:
                    solution.append(row)
                solution.append(f'score: {score}')
                solution.append('WIN: Ghost')
                break

            # Output Ghost move layout and score
            solution.append(f'{round_num}: W moving {ghost_move}')
            for row in layout:
                solution.append(row)
            solution.append(f'score: {score}')
            
    return '\n'.join(solution)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)