import collections, sys, parse, grader
from heapq import heappush, heappop

def astar_search(problem):
    #Your p5 code here
    startState = problem['start_state']
    goalState = problem['goal_states']
    heuristic = problem['heuristics']
    stateSpaceGraph = problem['transitions']
    frontier = []
    heappush(frontier, (heuristic[startState], startState))
    solutionPath = []
    heappush(solutionPath, (heuristic[startState], startState))
    exploredSet = collections.OrderedDict()
    # print('Initial frontier:',list(frontier)) 
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
            # print('Exploring:',lastnode,'at cost',node[0],'...')
            exploredSet[lastnode] = True
            if lastnode in stateSpaceGraph:
                for child in stateSpaceGraph[lastnode]: 
                    heappush(frontier, (node[0]+child[0]-heuristic[lastnode]+heuristic[child[1]], node[1]+child[1]))
                    heappush(solutionPath, (node[0]+child[0]-heuristic[lastnode]+heuristic[child[1]], path[1]+' '+child[1]))
            # else:
            #     print('No children for',lastnode)
            # print(list(frontier))
            # print(exploredSet.keys())
            # input()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)