"""
Contains the planning code that uses A* to connect the starting synset 
(the synset of the object chosen by the user) to the ending synset 
(the synset of the objetc on the table that is most similar to the object chosen by the user) 
this is used in the project because of the much faster runtime compared to the PDDL solver.
"""
from nltk.corpus import brown
import numpy as np
from collections import defaultdict
import random
from pprint import pprint
from nltk.corpus import wordnet
import nltk
nltk.download('wordnet')




from nltk.corpus import wordnet as wn
from queue import PriorityQueue




def heuristic_cost_estimate(start_synset, goal_synset):
    # Implement your heuristic function here
    return 1 - similarity(start_synset, goal_synset)

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

# with open("top_5000.txt") as f:
#     COMMON_WORDS = [x.replace("\n", "").strip() for x in f.readlines()]
# print(COMMON_WORDS)
def a_star(start_synset, goal_synset, children_mode=False):
    open_set = PriorityQueue()
    open_set.put((0, start_synset, '_'))

    came_from = {}
    relation_diz = {}
    g_score = {start_synset: 0}
    f_score = {start_synset: heuristic_cost_estimate(start_synset, goal_synset)}

    while not open_set.empty():
        _, current, synset_type = open_set.get()
        parts = current.name().split(".")[0].split("_")
        # if children_mode and any(part not in COMMON_WORDS for part in parts):
        #     cost = 1000
        # else:
        #     cost = 1
        cost = 1
        if current == goal_synset:
            relation_diz[current] = synset_type
            path = reconstruct_path(came_from, current, relation_diz)
            return path

        connected_synsets = get_connected_synsets(current)
        for neighbor, synset_type in connected_synsets:
            tentative_g_score = g_score[current] + cost  # Assuming all edges have a weight of 1

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                relation_diz[neighbor] = synset_type
                g_score[neighbor] = tentative_g_score
                # print(tentative_g_score)
                f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal_synset)
                # print(neighbor, goal_synset, heuristic_cost_estimate(neighbor, goal_synset))
                open_set.put((f_score[neighbor], neighbor, synset_type))

    return None  # No path found

def reconstruct_path(came_from, current, relation_diz):
    path = [(current, relation_diz[current])]
    while current in came_from:
        current = came_from[current]
        try:
            relation = relation_diz[current]
        except KeyError:
            relation = None
        path.append((current,relation))
    path.reverse()
    return path, relation_diz


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


def load_glove(dim=50):

    glove_dict = defaultdict(lambda: np.array([0.0 for _ in range(dim)]))

    file_name = '../glove_data/glove.6B.' + str(dim) + 'd.txt'
    with open(file_name) as f:
        for line in f:
            word, nums = line.replace('\n', '').split(' ', 1)

            glove_dict[word] = np.array([float(x) for x in nums.split(' ')])

    return glove_dict


glove_dict = load_glove(dim=50)


def similarity(word1, word2):
    word1_clean = word1.name().split('.')[0]
    word2_clean = word2.name().split('.')[0]

    word1_array = np.mean([glove_dict[subword1_clean]
                          for subword1_clean in word1_clean.split("_")], axis=0)
    word2_array = np.mean([glove_dict[subword2_clean]
                          for subword2_clean in word2_clean.split("_")], axis=0)
    # word1_array = glove_dict[word1_clean]
    # word2_array = glove_dict[word2_clean]

    # print(word1_array.shape)

    return np.dot(word1_array/(np.linalg.norm(word1_array) + 0.01), word2_array/(np.linalg.norm(word2_array) + 0.01))


def get_path_between_synsets(synset1, synset2):
    """
    This function given two synsets, finds the path between them, returning
    both the synsets encountered and the relations between the synsets encountered.
    """

    # Create a queue to perform breadth-first search
    queue = [(synset1, [])]
    seen = set([synset1.name().split(".")[0]])

    while queue:
        current_synset, path = queue.pop(0)
        connected_synsets = get_connected_synsets(current_synset)

        k = 200

        def sort_key(x):
            try:
                freq = common_words[x[0].name().split('.')[0]]
            except KeyError:
                freq = 100

            # + similarity(synset1, x[0])#(8.0 if x[1] in ("hypernym", "hyponym") else 0.0) + similarity(x[0], synset2)
            return similarity(x[0], synset2)

        all_connected = sorted([x for x in connected_synsets if x[0].name().split(".")[
                               0] not in seen], key=sort_key, reverse=True)
        if all_connected:
            # print(current_synset)
            # print(all_connected)
            pass

        seen = seen.union(set([x[0].name().split(".")[0]
                          for x in all_connected]))

        for synset, relation in all_connected[:k]:
            if synset == synset2:
                # Found the target synset, return the path
                return path + [(synset, relation)]
            else:
                # Add the synset to the queue for further exploration
                queue.append((synset, path + [(synset, relation)]))

    # If the loop completes without finding the target synset, return None
    return None


NAME_TO_COMMON_LANGUAGE = {
    "hypernym": " is a ",
    "meronym": " contains ",
    "holonym": " is a part of ",
    "hyponym": " could be a "

}


def generate_phrase(start, path):
    """
    This function generates natural language phrases based on the start synset,
    path containing synsets and relations, and creates triplets of start,
    relation, and end synsets.
    """
    # pprint(locals())
    phrase = start.name() + \
        NAME_TO_COMMON_LANGUAGE[path[0][1]] + path[0][0].name()

    for i, item in enumerate(path[1:], start=1):
        phrase += " " + path[i-1][0].name() + \
            NAME_TO_COMMON_LANGUAGE[item[1]] + item[0].name()
    return phrase


def generate_phrase2(start, path):
    """
    This function generates natural language phrases based on the start synset,
    path containing synsets and relations, and creates triplets of start,
    relation, and end synsets.
    """
    # pprint(locals())
    phrase = ""
    #phrase = start.name() + \
    #    NAME_TO_COMMON_LANGUAGE.get(path[0][1], " ") + path[0][0].name()

    for i, item in enumerate(path[1:], start=1):
        phrase += path[i-1][0].name() + \
            NAME_TO_COMMON_LANGUAGE.get(item[1], " ") + item[0].name() + ",\n"
    return phrase


# Example usage


word_pairs = [
    ('happy', 'joyful'),
    ('big', 'large'),
    ('hot', 'warm'),
    ('sad', 'unhappy'),
    ('fast', 'quick'),
    ('smart', 'intelligent'),
    ('funny', 'humorous'),
    ('beautiful', 'gorgeous'),
    ('angry', 'furious'),
    ('tired', 'exhausted'),
    ('apple', 'chair'),
    ('table', 'banana'),
    ('dog', 'television'),
    ('book', 'cup'),
    ('shoe', 'window'),
    ('car', 'lamp'),
    ('tree', 'computer'),
    ('pen', 'guitar'),
    ('flower', 'keyboard'),
    ('sun', 'desk')
]
synset_pairs = [
    ('fish.n.01', 'salmon.n.01'),
    ('dog.n.01', 'cat.n.01'),
    ('car.n.01', 'truck.n.01'),
    ('table.n.01', 'chair.n.01'),
    ('pen.n.01', 'pencil.n.01'),
    ('book.n.01', 'notebook.n.01'),
    ('tree.n.01', 'bush.n.01'),
    ('shoe.n.01', 'sandal.n.01'),
    ('cup.n.01', 'mug.n.01'),
    ('flower.n.01', 'plant.n.01'),
    ('bicycle.n.01', 'scooter.n.01'),
    ('hat.n.01', 'cap.n.01'),
    ('guitar.n.01', 'ukulele.n.01'),
    ('cookie.n.01', 'cracker.n.01'),
    ('ball.n.01', 'balloon.n.01'),
    ('watch.n.01', 'clock.n.01'),
    ('sock.n.01', 'glove.n.01'),
    ('door.n.01', 'window.n.01'),
    ('spoon.n.01', 'fork.n.01'),
    ('bed.n.01', 'couch.n.01')
]

strange_words = [
    ("xylophagous", "floccinaucinihilipilification"),
    ("sesquipedalian", "antidisestablishmentarianism"),
    ("hippopotomonstrosesquippedaliophobia",
     "pneumonoultramicroscopicsilicovolcanoconiosis"),
    ("supercalifragilisticexpialidocious", "honorificabilitudinitatibus"),
    ("schadenfreude", "sesquicentennial"),
    ("onomatopoeia", "epizootiologies"),
]


# print("START SEARCH...")

nltk.download('brown')  # Download the Brown Corpus


# Get frequency distribution of words in the Brown Corpus
word_freq = nltk.FreqDist(brown.words())

# Get the most common 1000 words along with their frequency
common_words = {k.lower(): v for k, v in word_freq.most_common(1000)}


# for a,b in strange_words:
#     print("{} is common?".format(a))
#     print(is_common_word(a))
#     print("{} is common?".format(b))
#     print(is_common_word(b))

def make_experiment(children_mode, filename):
    avg = 0
    with open(filename, "w+") as f:
        for pair in synset_pairs:

            w1, w2 = pair
            synset1 = wordnet.synset(w1)  # Replace with the first synset
            synset2 = wordnet.synset(w2)  # Replace with the second synset
        
            # path = get_path_between_synsets(synset1, synset2)
            path, synsets = a_star(synset1, synset2, children_mode=children_mode)
            f.write("path" + str(path) + "\n")
            avg += len(path)
            p = True
            if path:
                for synset, relation in path[:-1]:
                    f.write(str(synset)+"\n")
                    f.write(str(relation)+"\n")

            else:
                f.write("No path found between the synsets.\n")

            f.write(str(generate_phrase2(synset1, path))+"\n")
            f.write("\n\n\n")

        f.write(str(avg/float(len(synset_pairs)))+"\n")

if __name__ == "__main__":
    make_experiment(children_mode=True, filename="child_friendly_phrases.txt")
    make_experiment(children_mode=False, filename="normal_phrases.txt")