from nltk.corpus import wordnet
from pprint import pprint
import random

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

def get_path_between_synsets(synset1, synset2):
    """
    This function given two synsets, finds the path between them, returning
    both the synsets encountered and the relations between the synsets encountered.
    """

    # Create a queue to perform breadth-first search
    queue = [(synset1, [])]

    while queue:
        current_synset, path = queue.pop(0)
        connected_synsets = random.sample(get_connected_synsets(current_synset), k=len(get_connected_synsets(current_synset))//10 or 1)

        for synset, relation in connected_synsets:
            if synset == synset2:
                # Found the target synset, return the path
                return path + [(synset, relation)]
            else:
                # Add the synset to the queue for further exploration
                queue.append((synset, path + [(synset, relation)]))

    # If the loop completes without finding the target synset, return None
    return None


NAME_TO_COMMON_LANGUAGE = {
    "hypernym" : " is a ",
    "meronym" : " contains ",
    "holonym" : " is a part of ",
    "hyponym" : " could be a "

}
def generate_phrase(start, path):
    """
    This function generates natural language phrases based on the start synset,
    path containing synsets and relations, and creates triplets of start,
    relation, and end synsets.
    """
    pprint(locals())
    phrase = start.name() + NAME_TO_COMMON_LANGUAGE[path[0][1]] + path[0][0].name()

    for i, item in enumerate(path[1:], start=1):
        phrase += " " + path[i-1][0].name() + NAME_TO_COMMON_LANGUAGE[item[1]] + item[0].name()
    return phrase

# Example usage
synset1 = wordnet.synset('fish.n.01')  # Replace with the first synset
synset2 = wordnet.synset('salmon.n.01')  # Replace with the second synset
path = get_path_between_synsets(synset1, synset2)

if path:
    for synset in path:
        print(synset)
else:
    print("No path found between the synsets.")

print(generate_phrase(synset1, path))
print("\n\n\n")
synset1 = wordnet.synset('pen.n.01')  # Replace with the first synset
synset2 = wordnet.synset('pencil.n.01')  # Replace with the second synset
path = get_path_between_synsets(synset1, synset2)

if path:
    for synset in path:
        print(synset)
else:
    print("No path found between the synsets.")

synset1 = wordnet.synset('fish.n.01')  # Replace with the first synset
synset2 = wordnet.synset('boat.n.01')  # Replace with the second synset
path = get_path_between_synsets(synset1, synset2)

if path:
    for synset in path:
        print(synset)
else:
    print("No path found between the synsets.")

