import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
import random
from pprint import pprint
from nltk.corpus import wordnet
import re
import tqdm

FILE = """(define (problem connected-nodes-kinds-problem)
  (:domain connected-nodes-kinds-domain)
  
  (:objects
    {object_list}
  )
  
  (:init
    (at {initial})
{relation_list}
  )
  
  (:goal
    (at {goal})
  )
)"""

# Get all synsets in WordNet
synsets = list(wordnet.all_synsets())
random.shuffle(synsets)
c = 0



all_words = []
all_relations = []
pattern = re.compile("\.[a-z]\.[0-9][0-9]")
def make_relations_and_add_words(relations, string_name):
    relations_new = [(x.name(), string_name) for x in relations]
    # all_words_names = set([x if isinstance(x, str) else x.name() for x in all_words])
    all_words.extend([x[0] for x in relations_new if x[0] not in all_words])#_names])
    return relations_new


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


# Create a text file to save the synsets and their relations
with open('/home/peppe/Desktop/planning_test/pyperplan/wordnet_/wordnet_automatic_problem.txt', 'w') as file:
    # Function to write the connections between synsets
    def write_connections(label, connections):
        if connections:
            file.write(f"{label}:\n")
            for connection in connections:
                # print("CONNECTION", connection)
                if not pattern.search(connection[0]):
                    continue
                file.write(f"  {connection[0]}: {connection[1]}\n")
                all_relations.append((synset, *connection))

    # Iterate over each synset
    correct = 0
    for i, synset in tqdm.tqdm(list(enumerate(synsets))):
        #if "boat" not in synset.name():
        #    continue
        # print(i)
        if '.n.' not in synset.name():
            c+=1
            # print(c)
            continue 
        else:
            correct += 1
        if count_synset_connections(synset) < 50:
            continue


        all_words.append(synset.name())

        # Write synset ID and lemma names
        file.write(f"Synset: {synset.name()}\n")
        file.write(f"Lemma Names: {', '.join(synset.lemma_names())}\n")

        # Write hypernym connections
        hypernyms = make_relations_and_add_words(synset.hypernyms(), "hypernym")
        write_connections("Hypernyms", hypernyms)

        # Write hyponym connections
        hyponyms = make_relations_and_add_words(synset.hyponyms(), "hypernym")
        write_connections("Hyponym", hyponyms)

        # # Write meronym connections
        meronyms = make_relations_and_add_words(synset.part_meronyms(), "meronym")
        write_connections("Meronyms", meronyms)

        # # Write holonym connections (reverse of meronyms)
        holonyms = make_relations_and_add_words(synset.part_holonyms(), "holonym")
        write_connections("Holonyms", holonyms)
        antonyms = []
        # # Write antonym connections
        # for lemma in synset.lemmas():
        #   antonyms.extend(make_relations_and_add_words(lemma.antonyms(), "antonym"))
        #   write_connections("Antonyms", antonyms)

        # # Write attribute connections
        attributes = make_relations_and_add_words(synset.attributes(), "attribute")
        write_connections("Attributes", attributes)

        # # Write entailment connections
        entailments = make_relations_and_add_words(synset.entailments(), "entailment")
        write_connections("Entailments", entailments)

        # # Write cause connections
        causes = make_relations_and_add_words(synset.causes(), "cause")
        write_connections("Causes", causes)

        # Write related synsets connections
        # related_synsets = make_relations_and_add_words(synset.lemmas(), "related")
        # write_connections("Related Synsets", related_synsets)

        file.write('\n')

        # if c > 10000:
        #     break


START_SYNSET = "car_n_01"#random.choice(all_words).replace(".", "_")
END_SYNSET = "bike_n_01"#random.choice(all_words).replace(".", "_")

# pprint(all_words[:100])
# pprint(all_relations[:100])

def format_relations(relations):
    lines = []
    for relation in relations:
      first_synset, second_synset, relation_kind = relation
      lines.append(f"    (connected-{relation_kind} {first_synset.name().replace('.', '_')} {second_synset.replace('.', '_')})")
    return '\n'.join(lines)

def write_pddl_file(start, end, all_words, all_relations):
    with open("/home/peppe/Desktop/planning_test/pyperplan/wordnet_/wordnet_automatic_problem.pddl", "w+") as f:
        f.write(FILE.format(
        object_list=' '.join( (x if isinstance(x, str) else x.name()).replace('.', '_') for x in all_words),#replace(".", "")
        initial=start,
        relation_list=format_relations(all_relations),
        goal=end
    ))
          

all_words = [(x if isinstance(x, str) else x.name()).replace('.', '_') for x in all_words]

write_pddl_file(START_SYNSET, END_SYNSET, set(all_words), all_relations)