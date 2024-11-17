import collections, sys, grader, parse

def bfs_search(problem):
    #Your p2 code here
    startState = problem['start_state']
    goalState = problem['goal_states']
    heuristic = problem['heuristics']
    stateSpaceGraph = problem['transitions']
    frontier = collections.deque([startState])
    solutionPath = collections.deque([startState])
    exploredSet = collections.OrderedDict()
    # print('Initial frontier:',list(frontier)) 
    # input()
    while frontier:
        node = frontier.popleft()
        path = solutionPath.popleft()
        count = 0
        # ensures that pop node is in the explored set
        while(True):
            count = count - 1
            if node[count:] in heuristic:
                lastnode = node[count:]
                break
        if any(node.endswith(goal) for goal in goalState):
            my_set = ' '.join(exploredSet.keys())
            solution = my_set + '\n' + path
            return solution
        if lastnode not in exploredSet:
            # print('Exploring:',lastnode,'...')
            exploredSet[lastnode] = True
            if lastnode in stateSpaceGraph:
                for child in stateSpaceGraph[lastnode]: 
                    frontier.append(node+child[1])
                    solutionPath.append(path+' '+child[1])
            # else:
            #     print('No children for',lastnode)
            # print(list(frontier))
            # print(exploredSet.keys())
            # input()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)