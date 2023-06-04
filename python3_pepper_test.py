from PIL import Image
import requests
import os
from transformers import CLIPProcessor, CLIPModel
import sys

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

options = ["a photo of a cat", "a photo of a dog"]
inputs = processor(text=options, images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
print(list(zip(options, probs[0])))

pip = os.getenv('PEPPER_IP')

pport = 9559

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir + '/cmd_server')

from pepper_cmd import *
import pepper_cmd

url = "tcp://" + pip + ":" + str(pport)

OBJECT_ANGLES = {
     "Book of Short Stories" : -90,
     "Glass of water" : -60,
     "Pencil" : -30,
     "Computer" : 30,
     "Hat" : 60,
     "Glasses" : 90
}

def most_relevant_object(result, objects):
    return random.choice(list(objects))


def naoqiAPI():
    # session = qi.Session()

    # session.connect("tcp://{}:{}".format(pip, str(pport)))
    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session

    memory_service = app.session.service("ALMemory")

    motion_service = session.service("ALMotion")

    # ALDialog = session.service("ALDialog")

    # voice only
    tts_service = session.service("ALTextToSpeech")
    tts_service.setLanguage("English")
    tts_service.setParameter("speed", 90)
    tts_service.say("Hello, I am a curiosity bot!")
