import sys, parse, random
import time, os, copy
from collections import deque
EAT_FOOD_SCORE = 10 
PACMAN_EATEN_SCORE = -500 
PACMAN_WIN_SCORE = 500 
PACMAN_MOVING_SCORE = -1 

def expecti_max_multiple_ghosts(problem, k):
    #Your p6 code here
    seednum = problem['seed']
    layout = problem['layout'].split('\n')
    max_depth = k

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
    
    # bfs distance
    def bfs_distance(start, goal, layout):
        if start == goal:
            return 0
        
        rows, cols = len(layout), len(layout[0])
        queue = deque([(start, 0)])
        visited = set()
        visited.add(start)
        
        while queue:
            (current_x, current_y), distance = queue.popleft()
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_x, next_y = current_x + dx, current_y + dy
                
                if 0 <= next_x < rows and 0 <= next_y < cols and layout[next_x][next_y] != '%' and (next_x, next_y) not in visited:
                    if (next_x, next_y) == goal[0:2]:
                        return distance + 1
                    queue.append(((next_x, next_y), distance + 1))
                    visited.add((next_x, next_y))
        
        return float('inf')  # if no path found

    # find nearest Ghost and Food
    def find_nearest_ghost(pacman_pos, ghost_positions, layout):
        min_distance = float('inf')
        for ghost_pos in ghost_positions:
            distance = bfs_distance(pacman_pos, ghost_pos, layout)
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def find_nearest_food(pacman_pos):
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
    
    def find_positions(layout):
        # Find Pacman and Ghost positions
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

        return pacman_pos, ghost_positions
    
    def evaluation_function(pacman_pos, ghost_positions, layout):
        ghost_distance = find_nearest_ghost(pacman_pos, ghost_positions, layout)
        # ghost_total_distance = total_ghost_distance(pacman_pos, ghost_positions)
        food_distance = find_nearest_food(pacman_pos)
        
        # Calculate danger score based on nearest ghost
        if ghost_distance < 2:
            danger_score = -(2 - ghost_distance) * 10
        else:
            danger_score = 0
        
        score = ghost_distance/food_distance + danger_score
        
        return score
    
    def expectimax(state, depth, agent_index, max_depth):
        pacman_pos, ghost_positions, layout = state

        # Base case: reach max depth or game over
        if depth == max_depth:
            return evaluation_function(pacman_pos, ghost_positions, layout), None
        
        if agent_index == 0:
            # Pacman's turn: maximizing player
            return getMax(state, depth, max_depth, agent_index)
        else:
            # Ghost's turn: expectimax player
            return getExpecti(state, depth, max_depth, agent_index)

    def getMax(state, depth, max_depth, agent_index):
        pacman_pos, ghost_positions, layout = state
        best_value = float('-inf')
        best_move = None
        directions = move_pacman(layout)
        
        if not directions:
            return evaluation_function(pacman_pos, ghost_positions, layout), None
        
        random.shuffle(directions)  # add randomness
        
        for move in directions:
            new_pacman_pos = {
                'N': (pacman_pos[0] - 1, pacman_pos[1]),
                'S': (pacman_pos[0] + 1, pacman_pos[1]),
                'W': (pacman_pos[0], pacman_pos[1] - 1),
                'E': (pacman_pos[0], pacman_pos[1] + 1)
            }[move]

            # Update layout with new Pacman position
            new_layout = copy.deepcopy(layout)
            new_layout[pacman_pos[0]] = layout[pacman_pos[0]][:pacman_pos[1]] + ' ' + layout[pacman_pos[0]][pacman_pos[1]+1:]
            new_layout[new_pacman_pos[0]] = new_layout[new_pacman_pos[0]][:new_pacman_pos[1]] + 'P' + new_layout[new_pacman_pos[0]][new_pacman_pos[1]+1:]

            new_state = (new_pacman_pos, ghost_positions, new_layout)
            value, _ = expectimax(new_state, depth + 1, agent_index + 1, max_depth)
            
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_value, best_move

    def getExpecti(state, depth, max_depth, agent_index):
        pacman_pos, ghost_positions, layout = state
        expected_value = 0
        
        i, j, ghost_type = ghost_positions[agent_index - 1]
        directions = move_ghosts(layout, (i, j))
        
        if not directions:
            return evaluation_function(pacman_pos, ghost_positions, layout), None
        
        probability = 1 / len(directions)
        
        for move in directions:
            new_ghost_pos = {
                'N': (i - 1, j),
                'S': (i + 1, j),
                'W': (i, j - 1),
                'E': (i, j + 1)
            }[move]
            
            new_ghost_positions = [(new_ghost_pos[0], new_ghost_pos[1], ghost_type) if idx == agent_index - 1 else (x, y, t) for idx, (x, y, t) in enumerate(ghost_positions)]
            
            # Update layout with new Ghost position
            new_layout = copy.deepcopy(layout)
            new_layout[i] = layout[i][:j] + ' ' + layout[i][j+1:]
            new_layout[new_ghost_pos[0]] = new_layout[new_ghost_pos[0]][:new_ghost_pos[1]] + ghost_type + new_layout[new_ghost_pos[0]][new_ghost_pos[1]+1:]

            new_state = (pacman_pos, new_ghost_positions, new_layout)
            next_agent_index = (agent_index + 1) % (len(ghost_positions) + 1)
            value, _ = expectimax(new_state, depth + 1, next_agent_index, max_depth)
            
            expected_value += probability * value
        
        return expected_value, None
    
    # ················································main iteration·······························································
    # Find Pacman and Ghost positions
    pacman_pos, ghost_positions = find_positions(layout)

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
        
        # Pacman move
        _, pacman_move = expectimax((pacman_pos, ghost_positions, layout), 0, 0, max_depth)
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
            for ghost_index, ghost_pos in enumerate(ghost_positions):
                i, j, ghost_type = ghost_pos
                moves = move_ghosts(layout, (i, j))
                
                # Update layout
                if moves:
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
                    ghost_positions[ghost_index] = (new_ghost_pos[0], new_ghost_pos[1], ghost_type)

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
                    ghost_positions[ghost_index] = (i, j, ghost_type)
                    # Output Ghost move layout and score
                    solution.append(f'{round_num}: {ghost_type} moving ')
                    round_num += 1
                    for row in layout:
                        solution.append(row)
                    solution.append(f'score: {score}')
            
    return '\n'.join(solution), winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expecti_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)