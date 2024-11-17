import sys, parse, random
import time, os, copy
EAT_FOOD_SCORE = 10 
PACMAN_EATEN_SCORE = -500 
PACMAN_WIN_SCORE = 500 
PACMAN_MOVING_SCORE = -1 

def better_play_single_ghosts(problem):
    #Your p2 code here
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
    
    # manhattan distance
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # find nearest Ghost and Food
    def find_nearest_ghost(pacman_pos, ghost_pos):
        return manhattan_distance(pacman_pos, ghost_pos)

    def find_nearest_food(pacman_pos, layout):
        min_distance = float('inf')
        for i in range(len(layout)):
            for j in range(len(layout[0])):
                if layout[i][j] == '.':
                    distance = manhattan_distance(pacman_pos, (i, j))
                    if distance < min_distance:
                        min_distance = distance
        if min_distance == 0:
            return 0.01
        if min_distance == float('inf'):
            return 100
        return min_distance

    # find best move direction
    def best_direction(pacman_pos, ghost_pos, layout, directions):
        best_score = float('-inf')
        best_move = None
        
        for move in directions:
            new_pacman_pos = {
                'N': (pacman_pos[0] - 1, pacman_pos[1]),
                'S': (pacman_pos[0] + 1, pacman_pos[1]),
                'W': (pacman_pos[0], pacman_pos[1] - 1),
                'E': (pacman_pos[0], pacman_pos[1] + 1)
            }[move]
            
            ghost_distance = find_nearest_ghost(new_pacman_pos, ghost_pos)
            food_distance = find_nearest_food(new_pacman_pos, layout)

            # Calculate danger score based on nearest ghost
            if ghost_distance < 2:
                danger_score = -(2 - ghost_distance) * 10
            else:
                danger_score = 0
            
            score = ghost_distance/food_distance + danger_score
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    # ················································main iteration·······························································
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
    
    # output inintial seed value and layout
    winner = None
    solution = []
    solution.append(f'seed: {seednum}')
    solution.append(str(round_num))
    for row in layout:
        solution.append(row)
    
    while not game_over:
        # input()
        round_num += 1
        
        # get Pacman and Ghost move directions
        direction = move(layout)
        
        # Pacman move
        if direction['pacman']:
            pacman_move = best_direction(pacman_pos, ghost_pos, layout, direction['pacman'])
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
            
            # update Pacman position
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
                winner = 'Ghost'
                break

            # out Pacman move and layout
            solution.append(f'{round_num}: P moving {pacman_move}')
            round_num += 1
            
            for row in layout:
                solution.append(row)
                
            # Check if Pacman wins
            if next_char == ' ' and all('.' not in row for row in layout):
                score += PACMAN_WIN_SCORE
                game_over = True
                solution.append(f'score: {score}')
                solution.append('WIN: Pacman')
                winner = 'Pacman'
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

            # update Ghost new position
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
                winner = 'Ghost'
                break

            # putput Ghost move and layout
            solution.append(f'{round_num}: W moving {ghost_move}')
            for row in layout:
                solution.append(row)
            solution.append(f'score: {score}')
            
    return '\n'.join(solution), winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)