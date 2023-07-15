"""
Classifies and image from a list of choices by using CLIP.
Uses the files in `setup_data` for the options.
"""
import sys
from PIL import Image
import requests
import os
from transformers import CLIPProcessor, CLIPModel
import sys
import json


model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

with open("../setup_data/labels_to_synsets.json") as f:
    data = json.load(f)
    labels = list(data.keys())

with open("../setup_data/table_objects.json") as f:
    OBJECT_ANGLES = json.load(f)


image = Image.open("../"+sys.argv[1])


options = labels + list(OBJECT_ANGLES.keys())
inputs = processor(text=options, images=image,
                   return_tensors="pt", padding=True)

outputs = model(**inputs)
# this is the image-text similarity score
logits_per_image = outputs.logits_per_image
# we can take the softmax to get the label probabilities
probs = logits_per_image.softmax(dim=1)

print(list(zip(options, [x.item() for x in probs[0]])))
