# # -*- coding: utf-8 -*-
# """ generic A-Star path searching algorithm """


# import sortedcontainers # type: ignore

# # introduce generic type

# infinity = 1000000
# ################################################################################
# class SearchNode():
#     """Representation of a search node"""

#     __slots__ = ("data", "gscore", "fscore", "closed", "came_from", "in_openset")

#     def __init__(
#         self, data, gscore = infinity, fscore = infinity
#     ):
#         self.data = data
#         self.gscore = gscore
#         self.fscore = fscore
#         self.closed = False
#         self.in_openset = False
#         self.came_from = None

#     def __lt__(self, b):
#         """Natural order is based on the fscore value & is used by heapq operations"""
#         return self.fscore < b.fscore


# ################################################################################
# class SearchNodeDict():
#     """A dict that returns a new SearchNode when a key is missing"""

#     def __missing__(self, k):
#         v = SearchNode(k)
#         self.__setitem__(k, v)
#         return v


# ################################################################################


# class OpenSet():
#         def __init__(self):
#             self.sortedlist = sortedcontainers.SortedList(key=lambda x: x.fscore)

#         def push(self, item):
#             item.in_openset = True
#             self.sortedlist.add(item)

#         def pop(self):
#             item = self.sortedlist.pop(0)
#             item.in_openset = False
#             return item

#         def remove(self, item):
#             self.sortedlist.remove(item)
#             item.in_openset = False

# ################################################################################*

# class AStar():
#     __slots__ = ()

#     # @abstractmethod
#     # def heuristic_cost_estimate(self, current, goal):
#     #     """
#     #     Computes the estimated (rough) distance between a node and the goal.
#     #     The second parameter is always the goal.
#     #     This method must be implemented in a subclass.
#     #     """
#     #     raise NotImplementedError

#     # @abstractmethod
#     # def distance_between(self, n1, n2):
#     #     """
#     #     Gives the real distance between two adjacent nodes n1 and n2 (i.e n2
#     #     belongs to the list of n1's neighbors).
#     #     n2 is guaranteed to belong to the list returned by the call to neighbors(n1).
#     #     This method must be implemented in a subclass.
#     #     """

#     # @abstractmethod
#     # def neighbors(self, node):
#     #     """
#     #     For a given node, returns (or yields) the list of its neighbors.
#     #     This method must be implemented in a subclass.
#     #     """
#     #     raise NotImplementedError

#     # def is_goal_reached(self, current, goal):
#     #     """
#     #     Returns true when we can consider that 'current' is the goal.
#     #     The default implementation simply compares `current == goal`, but this
#     #     method can be overwritten in a subclass to provide more refined checks.
#     #     """
#     #     return current == goal

#     def reconstruct_path(self, last, reversePath=False):
#         def _gen():
#             current = last
#             while current:
#                 yield current.data
#                 current = current.came_from

#         if reversePath:
#             return _gen()
#         else:
#             return reversed(list(_gen()))

#     def astar(
#         self, start, goal, reversePath = False
#     ):
#         if self.is_goal_reached(start, goal):
#             return [start]

#         openSet = OpenSet()
#         searchNodes = SearchNodeDict()
#         startNode = searchNodes[start] = SearchNode(
#             start, gscore=0.0, fscore=self.heuristic_cost_estimate(start, goal)
#         )
#         openSet.push(startNode)

#         while openSet:
#             current = openSet.pop()

#             if self.is_goal_reached(current.data, goal):
#                 return self.reconstruct_path(current, reversePath)

#             current.closed = True

#             for neighbor in map(lambda n: searchNodes[n], self.neighbors(current.data)):
#                 if neighbor.closed:
#                     continue

#                 tentative_gscore = current.gscore + self.distance_between(
#                     current.data, neighbor.data
#                 )

#                 if tentative_gscore >= neighbor.gscore:
#                     continue

#                 neighbor_from_openset = neighbor.in_openset

#                 if neighbor_from_openset:
#                     # we have to remove the item from the heap, as its score has changed
#                     openSet.remove(neighbor)

#                 # update the node
#                 neighbor.came_from = current
#                 neighbor.gscore = tentative_gscore
#                 neighbor.fscore = tentative_gscore + self.heuristic_cost_estimate(
#                     neighbor.data, goal
#                 )

#                 openSet.push(neighbor)

#         return None




# def find_path(
#     start,
#     goal,
#     neighbors_fnct,
#     reversePath=False,
#     heuristic_cost_estimate_fnct = lambda a, b: 10000000,
#     distance_between_fnct = lambda a, b: 1.0,
#     is_goal_reached_fnct = lambda a, b: a == b,
# ):
#     """A non-class version of the path finding algorithm"""

#     class FindPath(AStar):
#         def heuristic_cost_estimate(self, current, goal):
#             return heuristic_cost_estimate_fnct(current, goal)  # type: ignore

#         def distance_between(self, n1, n2):
#             return distance_between_fnct(n1, n2)

#         def neighbors(self, node):
#             return neighbors_fnct(node)  # type: ignore

#         def is_goal_reached(self, current, goal):
#             return is_goal_reached_fnct(current, goal)

#     return FindPath().astar(start, goal, reversePath)


# __all__ = ["AStar", "find_path"]

from nltk.corpus import wordnet as wn
from queue import PriorityQueue

def heuristic_cost_estimate(start_synset, goal_synset):
    # Implement your heuristic function here
    return 0  # Default heuristic, always returns 0

def get_connected_synsets(synset):
    connected_synsets = []
    for hypernym in synset.hypernyms():
        connected_synsets.append((hypernym, "hypernym"))
    for hyponym in synset.hyponyms():
        connected_synsets.append((hyponym, "hyponym"))
    for meronym in synset.part_meronyms() + synset.substance_meronyms() + synset.member_holonyms():
        connected_synsets.append((meronym, "meronym"))
    for holonym in synset.part_holonyms() + synset.substance_holonyms() + synset.member_meronyms():
        connected_synsets.append((holonym, "holonym"))
    return connected_synsets

def a_star(start_synset, goal_synset):
    open_set = PriorityQueue()
    open_set.put((0, start_synset))

    came_from = {}
    g_score = {start_synset: 0}
    f_score = {start_synset: heuristic_cost_estimate(start_synset, goal_synset)}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal_synset:
            path = reconstruct_path(came_from, current)
            return path

        connected_synsets = get_connected_synsets(current)
        for neighbor, _ in connected_synsets:
            tentative_g_score = g_score[current] + 1  # Assuming all edges have a weight of 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal_synset)
                open_set.put((f_score[neighbor], neighbor))

    return None  # No path found

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

# Example usage:
start_synset = wn.synset('table.n.01')
goal_synset = wn.synset('boat.n.01')
path = a_star(start_synset, goal_synset)
if path:
    print("Path found:")
    for synset in path:
        print(synset)
else:
    print("No path found.")
