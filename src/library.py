"""
Utilities.
"""
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
    return eval(output)

def classify_text(text):
    stream = os.popen(
        'python3 classify_text3.py {}'.format(text))
    output = stream.read()
    return eval(output)



GLOVE = "glove.6B.zip"

if check_and_download_file(GLOVE, "../glove_data_download/", "https://nlp.stanford.edu/data/"+GLOVE):
    print("File already exists......")

unzip_file_if_needed("../glove_data_download/" + GLOVE, "../glove_data/")

WIKI = "simplewiki-20230520-pages-articles-multistream.xml.bz2"
if check_and_download_file(WIKI, "../wikipedia_data/", "https://dumps.wikimedia.org/simplewiki/20230520/" + WIKI):
    print("File simplewiki already exists......")

extract_multistream_bz2("../wikipedia_data/"+WIKI, "../simple_english_wiki/")



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

        wiki_data[title.lower()] = text
    return wiki_data


WIKI_DATA = make_title_dict("../wikipedia_data/"+WIKI)


