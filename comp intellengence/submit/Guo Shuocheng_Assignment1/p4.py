import collections, sys, parse, grader
from heapq import heappush, heappop

def greedy_search(problem):
    #Your p4 code here
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
        # ensures that pop node is in the explored set
        while(True):
            count = count - 1
            if node[1][count:] in heuristic:
                lastnode = node[1][count:]
                break
        if any(node[1].endswith(goal) for goal in goalState):
            my_set = ' '.join(exploredSet.keys())
            solution = my_set + '\n' + path[1]
            return solution
        if lastnode not in exploredSet:
            # print('Exploring:',lastnode,'at cost',node[0],'...')
            exploredSet[lastnode] = True
            if lastnode in stateSpaceGraph:
                for child in stateSpaceGraph[lastnode]: 
                    heappush(frontier, (heuristic[child[1]], node[1]+child[1]))
                    heappush(solutionPath, (heuristic[child[1]], path[1]+' '+child[1]))
            # else:
            #     print('No children for',lastnode)
            # print(list(frontier))
            # print(exploredSet.keys())
            # input()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    grader.grade(problem_id, test_case_id, greedy_search, parse.read_graph_search_problem)