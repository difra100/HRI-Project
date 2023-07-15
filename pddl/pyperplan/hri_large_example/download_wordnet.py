import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')


from nltk.corpus import wordnet

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
c = 0

all_words = []


# Create a text file to save the synsets and their relations
with open('wordnet_relations.txt', 'w') as file:
    # Function to write the connections between synsets
    def write_connections(label, connections):
        if connections:
            file.write(f"{label}:\n")
            for connection in connections:
                file.write(f"  {connection[0]}: {connection[1]}\n")

    # Iterate over each synset
    for synset in synsets:
        if '.n.' not in synset.name():
            c+=1
            # print(c)
            continue 
        # Write synset ID and lemma names
        file.write(f"Synset: {synset.name()}\n")
        file.write(f"Lemma Names: {', '.join(synset.lemma_names())}\n")

        # Write hypernym connections
        hypernyms = [(hypernym.name(), 'hypernym') for hypernym in synset.hypernyms()]
        write_connections("Hypernyms", hypernyms)

        # Write hyponym connections
        hyponyms = [(hyponym.name(), 'hyponym') for hyponym in synset.hyponyms()]
        write_connections("Hyponyms", hyponyms)

        # Write meronym connections
        meronyms = [(meronym.name(), 'meronym') for meronym in synset.part_meronyms()]
        write_connections("Meronyms", meronyms)

        # Write holonym connections (reverse of meronyms)
        holonyms = [(holonym.name(), 'holonym') for holonym in synset.part_holonyms()]
        write_connections("Holonyms", holonyms)

        # Write antonym connections
        antonyms = [(antonym.name(), 'antonym') for lemma in synset.lemmas() for antonym in lemma.antonyms()]
        write_connections("Antonyms", antonyms)

        # Write attribute connections
        attributes = [(attribute.name(), 'attribute') for attribute in synset.attributes()]
        write_connections("Attributes", attributes)

        # Write entailment connections
        entailments = [(entailment.name(), 'entailment') for entailment in synset.entailments()]
        write_connections("Entailments", entailments)

        # Write cause connections
        causes = [(cause.name(), 'cause') for cause in synset.causes()]
        write_connections("Causes", causes)

        # Write related synsets connections
        related_synsets = [(related.name(), 'related synset') for lemma in synset.lemmas() for related in lemma.synset().lemmas()]
        write_connections("Related Synsets", related_synsets)

        file.write('\n')

