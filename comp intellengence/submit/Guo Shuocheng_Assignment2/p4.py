import sys, parse, random
import time, os, copy
EAT_FOOD_SCORE = 10 
PACMAN_EATEN_SCORE = -500 
PACMAN_WIN_SCORE = 500 
PACMAN_MOVING_SCORE = -1 

def better_play_multiple_ghosts(problem):
    #Your p4 code here
    seednum = problem['seed']
    layout = problem['layout'].split('\n')

    def move_pacman(layout):
        n = len(layout)
        m = len(layout[0])
        
        # find Pacman position
        pacman_pos = None
        for i in range(n):
            for j in range(m):
                if layout[i][j] == 'P':
                    pacman_pos = (i, j)
                    break
            if pacman_pos:
                break
        
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
        
        pacman_moves.sort()
        return pacman_moves
    
    def move_ghosts(layout, ghost_pos):
        n = len(layout)
        m = len(layout[0])
        ghost_types = {'W', 'X', 'Y', 'Z'}

        # find Ghost move directions
        ghost_moves = []
        if ghost_pos:
            i, j = ghost_pos
            if i > 0 and layout[i-1][j] not in ghost_types and layout[i-1][j] != '%':  # North
                ghost_moves.append('N')
            if i < n-1 and layout[i+1][j] not in ghost_types and layout[i+1][j] != '%':  # South
                ghost_moves.append('S')
            if j > 0 and layout[i][j-1] not in ghost_types and layout[i][j-1] != '%':  # West
                ghost_moves.append('W')
            if j < m-1 and layout[i][j+1] not in ghost_types and layout[i][j+1] != '%':  # East
                ghost_moves.append('E')

        ghost_moves.sort()
        return ghost_moves
    
    # manhattan distance
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    # find nearest Ghost and Food
    def find_nearest_ghost(pacman_pos, ghost_positions):
        min_distance = float('inf')
        for ghost_pos in ghost_positions:
            distance = manhattan_distance(pacman_pos, ghost_pos)
            if distance < min_distance:
                min_distance = distance
        return min_distance

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
    def best_direction(pacman_pos, ghost_positions, layout, directions):
        best_score = float('-inf')
        best_move = None
        
        for move in directions:
            new_pacman_pos = {
                'N': (pacman_pos[0] - 1, pacman_pos[1]),
                'S': (pacman_pos[0] + 1, pacman_pos[1]),
                'W': (pacman_pos[0], pacman_pos[1] - 1),
                'E': (pacman_pos[0], pacman_pos[1] + 1)
            }[move]
            
            ghost_distance = find_nearest_ghost(new_pacman_pos, ghost_positions)
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
    ghost_positions = []
    ghost_types = {'W', 'X', 'Y', 'Z'}

    for i in range(len(layout)):
        for j in range(len(layout[0])):
            if layout[i][j] == 'P':
                pacman_pos = (i, j)
            elif layout[i][j] in ghost_types:
                ghost_positions.append((i, j, layout[i][j]))
    
    # Sort ghost_positions by ghost type to ensure the order W, X, Y, Z
    ghost_positions.sort(key=lambda x: x[2])
    
    score = 0
    game_over = False
    round_num = 1
    next_char = {}
    
    # Output initial seed value and layout
    winner = None
    solution = []
    solution.append(f'seed: {seednum}')
    solution.append('0')
    for row in layout:
        solution.append(row)
    
    while not game_over:
        # input()
        
        # Get Pacman and Ghost move directions
        pacman_moves = move_pacman(layout)
        
        # Pacman move
        if pacman_moves:
            pacman_move = best_direction(pacman_pos, ghost_positions, layout, pacman_moves)
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
            for ghost_pos in ghost_positions:
                if (ghost_pos[0], ghost_pos[1]) == pacman_pos:
                    score += PACMAN_EATEN_SCORE
                    game_over = True
                    layout[pacman_pos[0]] = layout[pacman_pos[0]][:pacman_pos[1]] + ghost_pos[2] + layout[pacman_pos[0]][pacman_pos[1]+1:]
                    solution.append(f'{round_num}: P moving {pacman_move}')
                    for row in layout:
                        solution.append(row)
                    solution.append(f'score: {score}')
                    solution.append('WIN: Ghost')
                    winner = 'Ghost'
                    break
            if game_over:
                break

            # Output Pacman move layout and score
            solution.append(f'{round_num}: P moving {pacman_move}')
            round_num += 1
            
            for row in layout:
                solution.append(row)
                
            # Check if Pacman wins
            # Check if next_char contains any '.' value
            if '.' not in next_char.values():
                if all('.' not in row for row in layout):
                    score += PACMAN_WIN_SCORE
                    game_over = True
                    solution.append(f'score: {score}')
                    solution.append('WIN: Pacman')
                    winner = 'Pacman'
                    break
            solution.append(f'score: {score}')
            
            
        # Ghost move
        if not game_over:
            # Move each Ghost in order
            new_ghost_positions = []
            for ghost_pos in ghost_positions:
                i, j, ghost_type = ghost_pos
                moves = move_ghosts(layout, (i, j))
                
                # Update layout
                if moves:
                    # Use random seed to choose a direction to move the Ghost
                    ghost_move = random.choice(moves)
                    new_ghost_pos = {
                        'N': (i - 1, j),
                        'S': (i + 1, j),
                        'W': (i, j - 1),
                        'E': (i, j + 1)
                    }[ghost_move]

                    if round_num == 1:
                        continue
                    else:
                        # Restore the position with food when the Ghost leaves
                        if next_char.get((i, j)) == '.':
                            layout[i] = layout[i][:j] + '.' + layout[i][j+1:]
                        else:
                            layout[i] = layout[i][:j] + ' ' + layout[i][j+1:]
                        
                        # delete the record 
                        if (i, j) in next_char:
                            del next_char[(i, j)]
                        
                    # Save the character at the new position where the Ghost is about to move
                    next_char[(new_ghost_pos[0], new_ghost_pos[1])] = layout[new_ghost_pos[0]][new_ghost_pos[1]]

                    # Update Ghost position
                    layout[new_ghost_pos[0]] = layout[new_ghost_pos[0]][:new_ghost_pos[1]] + ghost_type + layout[new_ghost_pos[0]][new_ghost_pos[1]+1:]
                    new_ghost_positions.append((new_ghost_pos[0], new_ghost_pos[1], ghost_type))

                    # Check if Ghost catches Pacman
                    if new_ghost_pos == pacman_pos:
                        score += PACMAN_EATEN_SCORE
                        game_over = True
                        solution.append(f'{round_num}: {ghost_type} moving {ghost_move}')
                        for row in layout:
                            solution.append(row)
                        solution.append(f'score: {score}')
                        solution.append('WIN: Ghost')
                        winner = 'Ghost'
                        break

                    # Output Ghost move layout and score
                    solution.append(f'{round_num}: {ghost_type} moving {ghost_move}')
                    round_num += 1
                    for row in layout:
                        solution.append(row)
                    solution.append(f'score: {score}')
                else:
                    # If the ghost cannot move, keep its current position
                    new_ghost_positions.append((i, j, ghost_type))
                    # Output Ghost move layout and score
                    solution.append(f'{round_num}: {ghost_type} moving ')
                    round_num += 1
                    for row in layout:
                        solution.append(row)
                    solution.append(f'score: {score}')
            
            # Update ghost_positions with new positions
            ghost_positions = new_ghost_positions
            
    return '\n'.join(solution), winner
    

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
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
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)