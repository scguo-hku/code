import collections, sys, parse, grader
from heapq import heappush, heappop

def ucs_search(problem):
    #Your p3 code here
    startState = problem['start_state']
    goalState = problem['goal_states']
    heuristic = problem['heuristics']
    stateSpaceGraph = problem['transitions']
    frontier = []
    heappush(frontier, (0, startState))
    solutionPath = []
    heappush(solutionPath, (0, startState))
    exploredSet = collections.OrderedDict()
    print('Initial frontier:',list(frontier)) 
    # input()
    while frontier:
        node = heappop(frontier)
        path = heappop(solutionPath)
        count = 0
        while(True):
            count = count - 1
            if node[1][count:] in heuristic:
                lastnode = node[1][count:]
                break
        if (node[1].endswith(goalState)): 
            my_set = ' '.join(exploredSet.keys())
            solution = my_set + '\n' + path[1]
            return solution
        if lastnode not in exploredSet:
            print('Exploring:',lastnode,'...')
            exploredSet[lastnode] = True
            if lastnode in stateSpaceGraph:
                for child in stateSpaceGraph[lastnode]: 
                    heappush(frontier, (node[0]+child[0], node[1]+child[1]))
                    heappush(solutionPath, (path[0]+child[0], path[1]+' '+child[1]))
            else:
                print('No children for',lastnode)
                # frontier.append(node)
            print(list(frontier))
            print(exploredSet.keys())
            # input()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)