
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

# # Example usage:
# start_synset = wn.synset('table.n.01')
# goal_synset = wn.synset('boat.n.01')
# print(start_synset, goal_synset)
# path = a_star(start_synset, goal_synset)
# if path:
#     print("Path found:")
#     for synset in path:
#         print(synset)
# else:
#     print("No path found.")
