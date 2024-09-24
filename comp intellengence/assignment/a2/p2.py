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
        
        # 找到 Pacman 和 Ghost 的位置
        pacman_pos = None
        ghost_pos = None
        for i in range(n):
            for j in range(m):
                if layout[i][j] == 'P':
                    pacman_pos = (i, j)
                elif layout[i][j] == 'W':
                    ghost_pos = (i, j)
        
        # 确定 Pacman 可以移动的方向
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
        
        # 确定 Ghost 可以移动的方向
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
        
        # 按字母表顺序排序
        pacman_moves.sort()
        ghost_moves.sort()
        
        # 输出 Pacman 和 Ghost 可以移动的方向
        direction = {
            'pacman': pacman_moves,
            'ghost': ghost_moves
        }

        return direction
    
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

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
        if min_distance == float('inf'):
            return 10000
        return min_distance

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
            
            score = ghost_distance - food_distance
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move

    
    # 找到 Pacman 和 Ghost 的位置
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
    
    # 输出初始 seed 值和布局
    winner = None
    solution = []
    solution.append(f'seed: {seednum}')
    solution.append(str(round_num))
    for row in layout:
        solution.append(row)
    
    while not game_over:
        # input()
        round_num += 1
        
        # 获取当前方向
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
            
            # 更新布局
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

            # 输出 Pacman 移动后的布局和得分
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
                # 更新 Ghost 离开的旧位置
                if next_char == '.':
                    layout[ghost_pos[0]] = layout[ghost_pos[0]][:ghost_pos[1]] + '.' + layout[ghost_pos[0]][ghost_pos[1]+1:]
                else:
                    layout[ghost_pos[0]] = layout[ghost_pos[0]][:ghost_pos[1]] + ' ' + layout[ghost_pos[0]][ghost_pos[1]+1:]
                
            # 保存 Ghost 即将移动到的新位置的字符
            next_char = layout[new_ghost_pos[0]][new_ghost_pos[1]]

            # 更新 Ghost 的新位置
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

            # 输出 Ghost 移动后的布局和得分
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