"""
Calculates the similarity between two texts by using CLIP.
Useful when the user enters the name of the object if image recognition failed.
"""
import torch
from torch.nn import CosineSimilarity
from transformers import CLIPTokenizer, CLIPModel, CLIPTextModel
import json
import sys

def calculate_similarity(text, labels):
    cossim = CosineSimilarity(dim=0, eps=1e-6)
    torch_device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = 'openai/clip-vit-base-patch32'

    tokenizer = CLIPTokenizer.from_pretrained(model_id)
    text_encoder = CLIPTextModel.from_pretrained(model_id).to(torch_device)
    model = CLIPModel.from_pretrained(model_id).to(torch_device)

    text_inputs = tokenizer(
        [text] + labels,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    ).to(torch_device)
    text_features = model.get_text_features(**text_inputs)
    text_embeddings = torch.flatten(text_encoder(text_inputs.input_ids.to(torch_device))['last_hidden_state'], 1, -1)

    similarities = []
    for i, label in enumerate(labels):
        similarity = cossim(text_features[0], text_features[i+1])
        similarities.append(similarity.item())

    return similarities


with open("../setup_data/table_objects.json") as f:
    file_json = json.load(f)


input_labels = list(file_json.keys())

input_text = sys.argv[1]


similarities = calculate_similarity(input_text, input_labels)
print(list(zip(input_labels, similarities)))