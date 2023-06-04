import torch
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
import json
from PIL import Image
from utils import *
import zipfile
from pprint import pprint
import xml.etree.ElementTree as ET
import os


def get_secarg(tup):
    return tup[-1]

def classify_image(image_path):
    stream = os.popen(
        'python3 classify_image3.py {}'.format(image_path))
    output = stream.read()
    print(locals())
    return eval(output)


def model_run(model, imagepath):
    image_path = imagepath
    image = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225])
    ])
    input_tensor = preprocess(image)
    input_batch = input_tensor.unsqueeze(0)

    # Run the input through the model
    with torch.no_grad():
        output = model(input_batch)
    return output


def predict_top1(model, imagepath, labels):
    # Preprocess the input image
    output = model_run(model, imagepath)
    max_score, predicted_idx = torch.max(
        torch.nn.functional.softmax(output, dim=-1), 1)
    predicted_label = labels[predicted_idx.item()]
    return predicted_label, max_score.item()


def predict_top_k(model, imagepath, labels, k=5):
    # Preprocess the input image
    output = model_run(model, imagepath)
    _, predicted_indices = torch.topk(output, k)

    predictions = []
    for idx in predicted_indices.squeeze():
        predicted_label = labels[idx.item()]
        predicted_score = output[0][idx].item()
        predictions.append((predicted_label, predicted_score))

    return predictions


GLOVE = "glove.6B.zip"

if check_and_download_file(GLOVE, "", "https://nlp.stanford.edu/data/"+GLOVE):
    print("File already exists......")

unzip_file_if_needed(GLOVE, "glove/")

# if check_and_download_file("corpus.tgz", "", "https://github.com/LGDoor/Dump-of-Simple-English-Wiki/raw/master/corpus.tgz"):
#     print("File already exists......")

# un_tgz_file_if_needed("corpus.tgz", "simple_english_wikipedia/")
WIKI = "simplewiki-20230520-pages-articles-multistream.xml.bz2"
if check_and_download_file(WIKI, "", "https://dumps.wikimedia.org/simplewiki/20230520/" + WIKI):
    print("File simplewiki already exists......")

extract_multistream_bz2(WIKI, "simple_english_wiki/")

labels_path = 'labels_imgnet.json'
with open(labels_path) as f:
    labels = json.load(f)

# Load pre-trained ResNet50 model
model = models.resnet50(pretrained=True)
# model = models.regnet_y_128gf(weights=models.RegNet_Y_128GF_Weights)
model.eval()

# @persistent_disk_memoize


def parse_wiki(filename):
    return ET.parse(filename.replace(".bz2", ""), parser=ET.XMLParser(encoding='iso-8859-5'))


@persistent_disk_memoize
def make_title_dict(filename):
    tree = parse_wiki(filename)

    # Parse the XML file
    root = tree.getroot()

    # Define the namespace
    namespace = {'mw': 'http://www.mediawiki.org/xml/export-0.10/'}

    wiki_data = {}
    # Iterate over each 'page' element
    for page in root.findall('mw:page', namespace):
        # Extract the title
        title = page.find('mw:title', namespace).text

        # Extract the text
        text = page.find('mw:revision/mw:text', namespace).text

        # Print the title and text
        # print('Title:', title)
        # print('Text:', text)
        # print('---')

        wiki_data[title.lower()] = text
    return wiki_data


WIKI_DATA = make_title_dict(WIKI)

if __name__ == '__main__':

    pred = predict_top1(model, 'grace_hopper.jpg', labels)
    print("PRED IS: ", pred)
    # clean_string(wiki_data[pred]))#.split("\n\n")[1]))
    print(WIKI_DATA[pred])

# pprint(wiki_data)
# for page_element in root.iter("page"):
#     print(page_element)


# page_dict = {}
# for page in root.findall('page'):
#     print("PAGE: ", page)
#     title = page.find('title').text
#     print("Title: ", title)
#     page_text = page.find('text').text
#     page_dict[title] = page_text

# # Print the dictionary
# for title, page in page_dict.items():
#     print("Title:", title)
#     print("Page:", page)
#     print()
# with open("simple_english_wikipedia/corpus.txt") as f:
#     content = f.read()
#     articles = content.split("\n\n")
#     corpus = {}
#     for article in articles:
#         title, text = article.split("\n", 1)
#         corpus[title.lower()] = text

# # print(predict_top1("grace_hopper_517x606.jpg", labels))
# preds = predict_top_k(model, "grace_hopper_517x606.jpg", labels, k = 10)

# for pred, score in preds:
#     if pred.lower().replace(" ", "") in corpus:
#         print(corpus[pred.lower().replace(" ", "")])
