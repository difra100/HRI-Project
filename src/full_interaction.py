"""
A full interaction with the robot, see the report for more details.
"""
import time
import os
import sys
import qi
import math
import random
import math
import json
import library
from synsets_exploration import a_star, generate_phrase2
from nltk.corpus import wordnet
import nltk
from camera_photo import capture_image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pepper_motion import *

nltk.download('wordnet')
pip = os.getenv('PEPPER_IP')

pport = 9559

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir + '/cmd_server')

from pepper_cmd import *
import pepper_cmd

url = "tcp://" + pip + ":" + str(pport)

with open("../setup_data/table_objects.json") as f:
    OBJECT_ANGLES = json.load(f)

def most_relevant_object(result, objects):
    return random.choice(list(objects))

with open("../setup_data/labels_to_synsets.json") as f:
    PRED_TO_SYNSET = json.load(f)
    labels = sorted(list(PRED_TO_SYNSET.keys()))

import re
def clean_wiki(result, children_mode):
    # Remove everything in <ref> </ref>
    regex = r"\<ref\>(.*?)\<\/ref\>"
    result = re.sub(regex, "", result, flags =  re.DOTALL)

    # Remove everything in {{}}
    regex = r"\{\{(.*?)\}\}"
    result = re.sub(regex, "", result, flags =  re.DOTALL)

    # Remove references
    reg = r"&lt;ref&gt;(.*?)&lt;\/ref&gt;"
    result = re.sub(reg, "", result)
    # Remove references to files:
    file_regex = r"\[\[File\:.*\]\]"
    result = re.sub(file_regex, "", result)
    # Now substitute different named links: [[air pollution|polluted]] -> polluted
    regex = r"\[\[((?:(?!\]).)*?\|.*?)\]\]"
    intermediate_result1 = re.sub(regex, lambda x: x.group(1).split("|")[1], result)

    # Now substitute normal links [[cat]] -> [[cat]]
    regex = r"\[\[(.*?)\]\]"
    cleaned_result = re.sub(regex, r"\1", intermediate_result1)

    introduction_only = re.split("\=\=.*\=\=", cleaned_result)[0]

    final = ""
    maxlen = 300
    if children_mode:
        maxlen /= 2

    for phrase in introduction_only.split("."):
        if len(final) < maxlen:
            final += phrase + '.'
    return final.replace("'''", "")

def conclude_conversation(session, service, configuration):
    move_and_say(text = "Do you want to show me anything else?",robot = session, service = service, configuration = configuration, motion = 1)
    response = False
    answ = raw_input("<< Choose Yes or No >>")
    answ = answ.lower()

    if answ == "no" or answ == "n":
        move_and_say(text = "It has been a pleasure interacting with you!",robot = session, service = service, configuration = configuration, motion = 2)
        move_and_say(text = "Bye bye. Can't wait to talk with you again.",robot = session, service = service, configuration = configuration, motion = 0)
        response = True
    return response







def naoqiAPI():
    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session
    ALMotion = session.service("ALMotion")

    memory_service = app.session.service("ALMemory")

    motion_service = session.service("ALMotion")


    configuration = {"bodyLanguageMode":"disabled"}
    
    # voice only
    tts_service = session.service("ALAnimatedSpeech")


    move_and_say(text = "Hello, I am a curiosity bot!", robot = session, service = tts_service, configuration = configuration, motion = 0)
    
    move_and_say(text = "How old are you?", robot = session, service = tts_service, configuration = configuration, motion = 1)

    age = raw_input("Enter a number for your age > ")

    children_mode = False
    if int(age) < 10:
        children_mode = True
        move_and_say(text = "Aw, well, you are so young!", robot = session, service = tts_service, configuration = configuration, motion = 3)
    else:
        move_and_say(text = "Ah ok, so you are old enough to understand more complex explanation.", robot = session, service = tts_service, configuration = configuration, motion = 2)

    move_and_say(text = "If you show me something i can tell you some facts about it.", robot = session, service = tts_service, configuration = configuration, motion = 1)
    
    improve_image_msg = " please try to improve room lighting and put the object closer to the camera,"
    range_to_message = {
        (95, 100): "I am really sure that this is ",
        (80, 95): "I am quite sure that this is",
        (50, 80): "I think that it is quite probable that this is",
        (30, 50): "I am a bit confused,"+improve_image_msg+"maybe this is...",
        (0, 30): "I am really confused"+improve_image_msg+"I can guess that the object is...",
    }

    n_tab_obj = len(OBJECT_ANGLES)

    iteration = 0
    
    while True:
        modality = "image"
        iteration += 1
        move_and_say(text = "Touch my head when you are ready.......", robot = session, service = tts_service, configuration = configuration, motion = 1)


        raw_input("Press enter in the terminal to take a photo in this demo > ")

        filename = 'images/captured_image_' + str(iteration) + '.jpg'
        
        
        
        # capture_image(filename)


        time.sleep(5) # 10

       
        img_input = filename
        img_path = filename

        pred = library.classify_image(img_path)
        real_obj_len = len(pred) - n_tab_obj
        
        real_preds = pred[:real_obj_len]
        table_preds = pred[real_obj_len:]


        sorted_real_preds = sorted(real_preds, key = library.get_secarg, reverse = True)
        sorted_table_preds = sorted(table_preds, key = library.get_secarg, reverse = True)

        pred, score = sorted_real_preds[0]
        best_object, score_table = sorted_table_preds[0]

        sum_real = sum([x[1] for x in sorted_real_preds])
        sum_table = sum([x[1] for x in sorted_table_preds])

        score /= sum_real
        score_table /= sum_table

        
        # Maybe if really low score, then do not give prediction but loop and ask again
        for threshold in range_to_message.keys():
            if threshold[0] < score * 100 < threshold[1]:
                msg = range_to_message[threshold]
        
        # Uncertainty on the prediction (below 95%)
        if score*100 < 95:

            move_and_say(text = msg + " {}. Do you agree?".format(pred), robot = session, service = tts_service, configuration = configuration, motion = 1)
            
            answ = raw_input("<< Choose Yes or No >>")
            answ = answ.lower()

            if answ == "yes" or answ == "y":
                pass
            else:
                move_and_say(text = "I am sorry for the confusion. Do you want to show me the object again, or tell me what it is?", robot = session, service = tts_service, configuration = configuration, motion = 3)

                answ_obj = raw_input("<< (1) Show the object again; (2) Write the name >>")

                if answ_obj == "1":
                    continue
                else:
                    modality = "text"
                    name = raw_input("<< Enter the object's name >>")

                    p = random.random()

                    new_msg = "Oh, the object was {}....".format(name)
                    
                    if name not in PRED_TO_SYNSET:
                        move_and_say(text = "I do not know what a {} is. I am really sorry.".format(name),robot = session, service = tts_service, configuration = configuration, motion = 3)
                        response = conclude_conversation(session, tts_service, configuration)
                        if response:
                            break
                        else:
                            continue


            

                    if p > 0.5:
                        new_msg += " I thought to something similar."
                    else:
                        new_msg += " I had no idea."
                    

                    
                    
                move_and_say(text = new_msg, robot = session, service = tts_service, configuration = configuration, motion = 3)
                
            


             
        else:
            move_and_say(text = msg + " {}.".format(pred), robot = session, service = tts_service, configuration = configuration, motion = 1)

            print("The confidence for {} is equals to {}%".format(pred, round(score*100)))

        if modality == "text":
            result = library.classify_text(name)
            best_object, score_table = max(result, key = lambda x: x[1])
            pred = name
        msg = 'Unfortunately I have nothing interesting to say about this.'
        result = ""

        try:

            result = library.WIKI_DATA[pred]
        except KeyError:
            move_and_say(text = msg, robot = session, service = tts_service, configuration = configuration, motion = 2)

        if '#redirect' in result.lower():
            move_and_say(text = msg, robot = session, service = tts_service, configuration = configuration, motion = 2)

        elif result:
            move_and_say(text = "Let me tell you something about it...",robot = session, service = tts_service, configuration = configuration, motion = 2)

            result = clean_wiki(result, children_mode=children_mode)

  
            tts_service.say(result, configuration)

    
        angle, table_synset = OBJECT_ANGLES[best_object]
        explanation = str(round(score_table*100, 4)) # to do, do from best_object, should be a return value from most_relevant_object

      
        # for testing
        
        motion_service.moveTo(0.0, 0.0, math.radians(90))
        motion_service.moveTo(0.0, 0.0, math.radians(- 180))
        motion_service.moveTo(0.0, 0.0, math.radians(angle + 90))
        point_at_object(ALMotion)
        if table_synset != PRED_TO_SYNSET[pred]:
                print("The association with {} has a confidence of {}%".format(best_object, explanation))
                
        motion_service.moveTo(0, 0.0, math.radians(-angle))

        synset1 = wordnet.synset(PRED_TO_SYNSET[pred.lower()]) # use dict instead
        synset2 = wordnet.synset(table_synset)
        path, synsets = a_star(synset1, synset2, children_mode = children_mode)
        phrase = generate_phrase2(pred, path)

        phrase = phrase.replace("_", " ")
        phrase = re.sub("\.n\.[0-9]+", "", phrase) # otherwise get definition
        
        if phrase:
            move_and_say(text ="Let me tell you why your object and mine are connected.",robot = session, service = tts_service, configuration = configuration, motion = 1)
            move_and_say(text =phrase,robot = session, service = tts_service, configuration = configuration, motion = 2)
        
        else:
            move_and_say(text ="I also have a " + pred.lower() + " on my table.",robot = session, service = tts_service, configuration = configuration, motion = 2)

         
        response = conclude_conversation(session, tts_service, configuration)
        if response:
            break
        else:
            continue

            





if __name__ == "__main__":
    print(os.getenv('PEPPER_TOOLS_HOME'))
    naoqiAPI()
