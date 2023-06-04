import sys

from PIL import Image
import requests
import os
from transformers import CLIPProcessor, CLIPModel
import sys
import json


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

labels = [
    "book: a list of pages"
    "book: (verb) to pay in advance",
    "pen",
    "flask",
    "glasses",
    "old man",
    "guitar",
    "bird",
    "wall",
    "computer",
    "tissues",
    "smartphone",
    "bass guitar"
]

with open("table_objects.json") as f:
    OBJECT_ANGLES = json.load(f)


image = Image.open(sys.argv[1])


options = labels + list(OBJECT_ANGLES.keys())
inputs = processor(text=options, images=image,
                   return_tensors="pt", padding=True)

outputs = model(**inputs)
# this is the image-text similarity score
logits_per_image = outputs.logits_per_image
# we can take the softmax to get the label probabilities
probs = logits_per_image.softmax(dim=1)

print(list(zip(options, [x.item() for x in probs[0]])))