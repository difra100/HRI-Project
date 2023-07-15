from nltk.corpus import wordnet
from pprint import pprint
def count_synset_connections(synset):
    connections = {
        'hyponyms': synset.hyponyms(),
        'hypernyms': synset.hypernyms(),
        'meronyms': synset.part_meronyms() + synset.substance_meronyms() + synset.member_meronyms(),
        'holonyms': synset.part_holonyms() + synset.substance_holonyms() + synset.member_holonyms(),
        'entailments': synset.entailments(),
        'antonyms': synset.lemmas()[0].antonyms(),
    }

    pprint(connections)

    connection_lengths = {}
    for connection_type, synsets in connections.items():
        connection_lengths[connection_type] = len(synsets)

    return sum(connection_lengths.values())


# Example usage
synset = wordnet.synsets('car')[0]  # Example synset for 'car'
connections = count_synset_connections(synset)
print(connections)