# Code referenced from - https://www.redblobgames.com/pathfinding/a-star/implementation.html
import math
import heapq

# using this as my heuristic estimate
# calculates straight line distance between any 2 points
def get_distance_cost(refernce_map, from_point, to_point):
    (x1, y1) = refernce_map.intersections.get(from_point)
    (x2, y2) = refernce_map.intersections.get(to_point)
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )

# to store nodes with respect to total cost
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

# to return path in the expected format
def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    # need to reverse the order to have it from start to end
    path.reverse()
    return path


def shortest_path(M,start,goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in M.roads[current]:
            new_cost = cost_so_far[current] + get_distance_cost(M, current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                # using heuristic by getting distance from the node to goal
                priority = new_cost + get_distance_cost(M, next, goal)
                frontier.put(next, priority)
                came_from[next] = current
    

    print("shortest path called")
    return reconstruct_path(came_from, start, goal)