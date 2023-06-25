#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-import library
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
# from touch_handle import *
from camera_tests import capture_image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

nltk.download('wordnet')
pip = os.getenv('PEPPER_IP')

pport = 9559

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir + '/cmd_server')

from pepper_cmd import *
import pepper_cmd

url = "tcp://" + pip + ":" + str(pport)

with open("data/table_objects.json") as f:
    OBJECT_ANGLES = json.load(f)

def most_relevant_object(result, objects):
    return random.choice(list(objects))

with open("data/labels_to_synsets.json") as f:
    PRED_TO_SYNSET = json.load(f)
    labels = sorted(list(PRED_TO_SYNSET.keys()))

import re
def clean_wiki(result):
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

    # regex = r"\|(.*?)\]\]"
    # intermediate_result = re.sub(regex, r"\1", intermediate_result1)

    # Now substitute normal links [[cat]] -> [[cat]]
    regex = r"\[\[(.*?)\]\]"
    cleaned_result = re.sub(regex, r"\1", intermediate_result1)

    introduction_only = re.split("\=\=.*\=\=", cleaned_result)[0]

    final = ""
    maxlen = 300
    for phrase in introduction_only.split("."):
        if len(final) < maxlen:
            final += phrase + '.'
    return final.replace("'''", "")
test_article = """'''Air''' is the [[Earth]]'s [[atmosphere]]. Air is a [[mixture]] of many gases and tiny dust particles. It is the clear [[gas]] in which living things live and [[breathe]]. It has an indefinite shape and [[volume]]. It has [[mass]] and [[weight]], because it is [[matter]]. The weight of air creates [[atmosphere pressure|atmospheric pressure]]. There is no air in [[outer space]].

Air can be [[air pollution|polluted]] by some gases (such as [[carbon monoxide]], hydrocarbons, and nitrogen oxides), [[smoke]], and ash. This [[air pollution]] causes various problems including [[smog]], [[acid rain]] and [[global warming]]. It can damage people's [[health]] and the environment. There are debates about whether or not to act upon climate change, but soon enough the Earth will heat up to much, causing our home to become too hot and not support life! Some say fewer people would die of cold weather, and that is true but there is already a huge amount of people dying from heat and that number is and will keep increasing at a frighting height.

Since early times, air has been used to create [[technology]]. Ships moved with sails and windmills used the mechanical motion of air. Aircraft use [[propeller]]s to move air over a [[wing]], which allows them to [[flight|fly]]. [[Pneumatics]] use [[air pressure]] to move things. Since the late 1900s, air power is also used to generate electricity.

Air is invisible: it cannot be seen by the eye, though a shimmering in hot air can be seen.&lt;ref&gt;{{cite web | url=https://www.sciencefocus.com/planet-earth/why-is-air-invisible/ | title=Why is air invisible? }}&lt;/ref&gt;

Air is one of the 4 classical elements.
[[File:Sauerstoffgehalt-1000mj2.png|thumb|Oxygen content of the atmosphere over the last billion years&lt;ref&gt;{{cite journal |last1=Martin |first1=Daniel |last2=McKenna |first2=Helen |last3=Livina |first3=Valerie |title=The human physiological impact of global deoxygenation |journal=The Journal of Physiologica |doi=10.1007/s12576-016-0501-0 |pmid=27848144 |pmc=5138252 |issn=1880-6546 |year=2016 |volume=67 |issue=1 |pages=97–106 }}&lt;/ref&gt;&lt;ref&gt;[http://www.nap.edu/openbook/0309100615/gifmid/30.gif http://www.nap.edu/openbook/0309100615/gifmid/30.gif]&lt;/ref&gt;]]

== Brief history ==
Earth's atmosphere has changed much since its formation.

=== ''Original atmosphere'' ===
At first it was mainly a [[hydrogen]] atmosphere. It has changed dramatically on several occasions—for example, the [[Great Oxygenation Event]] 2.4 [[1,000,000,000|billion]] years ago, greatly increased [[oxygen]] in the atmosphere from practically no oxygen to levels closer to present day. Humans have also contributed to significant changes in atmospheric composition through air pollution, especially since [[industrialisation]], leading to rapid environmental change such as ozone depletion and global warming.

=== Second atmosphere ===
Outgassing from [[volcanism]], supplemented by gases produced during the [[Late Heavy Bombardment|late heavy bombardment]] of Earth by huge asteroids, produced the next atmosphere, consisting largely of [[nitrogen]] plus [[carbon dioxide]] and [[inert gas]]es.&lt;ref&gt;Zahnle K; Schaefer L; &amp; Fegley B. 2010. Earth's earliest atmospheres. Cold Spring Harbor Perspectives in Biology. 2 (10). PMID 20573713&lt;/ref&gt;

=== Third atmosphere ===
[[File:Sauerstoffgehalt-1000mj2.png|thumb|Oxygen content of the atmosphere over the last billion years&lt;ref&gt;{{cite journal |last1=Martin |first1=Daniel |last2=McKenna |first2=Helen |last3=Livina |first3=Valerie |title=The human physiological impact of global deoxygenation |journal=The Journal of Physiologica |doi=10.1007/s12576-016-0501-0 |pmid=27848144 |pmc=5138252 |issn=1880-6546 |year=2016 |volume=67 |issue=1 |pages=97–106 }}&lt;/ref&gt;&lt;ref&gt;[http://www.nap.edu/openbook/0309100615/gifmid/30.gif http://www.nap.edu/openbook/0309100615/gifmid/30.gif]&lt;/ref&gt;]]

The constant re-arrangement of continents by [[plate tectonics]] influences the long-term evolution of the atmosphere. Carbon dioxide was transferred to and from large continental carbonate stores. Free oxygen did not exist in the atmosphere until about 2.4 billion years ago. The [[Great Oxygenation Event]] is shown by the end of the [[banded iron formation]]s.
"""

cleaned_article = """'''Air''' is the Earth's atmosphere. Air is a mixture of many gases and tiny dust particles. It is the clear [[gas]] in which living things live and [[breathe]]. It has an indefinite shape and [[volume]]. It has [[mass]] and [[weight]], because it is [[matter]]. The weight of air creates atmospheric pressure. There is no air in outer space.

Air can be polluted by some gases (such as carbon monoxide, hydrocarbons, and nitrogen oxides), [[smoke]], and ash. This [[air pollution]] causes various problems including [[smog]], [[acid rain]] and [[global warming]]. It can damage people's [[health]] and the environment. There are debates about whether or not to act upon climate change, but soon enough the Earth will heat up to much, causing our home to become too hot and not support life! Some say fewer people would die of cold weather, and that is true but there is already a huge amount of people dying from heat and that number is and will keep increasing at a frighting height.

Since early times, air has been used to create technology. Ships moved with sails and windmills used the mechanical motion of air. Aircraft use [[propeller]]s to move air over a [[wing]], which allows them to [[flight|fly]]. [[Pneumatics]] use [[air pressure]] to move things. Since the late 1900s, air power is also used to generate electricity.

Air is invisible: it cannot be seen by the eye, though a shimmering in hot air can be seen.&lt;ref&gt;{{cite web | url=https://www.sciencefocus.com/planet-earth/why-is-air-invisible/ | title=Why is air invisible? }}&lt;/ref&gt;

Air is one of the 4 classical elements."""

# print("ORIGINAL:")
# print(test_article)
# print("GOLD CLEANED:")
# print(cleaned_article)
# print("OUR CLEANED:")
# print(clean_wiki(test_article))

def point_at_object(motion):
    names = []
    times = []
    keys = []

    names.append("RShoulderPitch")
    times.append([1.0, 2.0, 3.0])
    keys.append([1.0, -0.2, 0.8])

    motion.angleInterpolation(names, keys, times, True)

def handle_touch(touch_service, memory_service):
    while True:
        sl = touch_service.getSensorList() # vector of sensor names
        # print(sl)
        v = touch_service.getStatus()  # vector of sensor status [name, bool]
        # print(v)

        # print("STATUS")
        for a, b, c in v:
            if b == True:
                print("TOUCHED")


def naoqiAPI():
    # session = qi.Session()

    # session.connect("tcp://{}:{}".format(pip, str(pport)))
    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session
    ALMotion = session.service("ALMotion")

    memory_service = app.session.service("ALMemory")

    motion_service = session.service("ALMotion")

    # ALDialog = session.service("ALDialog")

    # voice only
    tts_service = session.service("ALTextToSpeech")
    tts_service.setLanguage("English")
    tts_service.setParameter("speed", 90)
    tts_service.say("Hello, I am a curiosity bot!")
    # time.sleep(1)

    # touch_service = session.service("ALTouch")
    # handle_touch(touch_service, memory_service)
    
    # touch_obj = ReactToTouch(session)
    tts_service.say("How old are you?")
    age = raw_input("Enter a number for your age > ")

    children_mode = False
    if int(age) < 10:
        children_mode = True
        tts_service.say("Aw, well, you are so young!")

    tts_service.say(
        "If you show me something i can tell you some facts about it.")
    # time.sleep(1.5)

    improve_image_msg = " please try to improve room lighting and put the object closer to the camera,"
    range_to_message = {
        (90, 100): "I am really sure that this is",
        (80, 90): "I am quite sure that this is",
        (50, 80): "I think that it is quite probable that this is",
        (30, 50): "I am a bit confused,"+improve_image_msg+"maybe this is...",
        (0, 30): "I am really confused"+improve_image_msg+"I can guess that the object is...",
    }

    n_tab_obj = len(OBJECT_ANGLES)

    iteration = 0
    while True:
        iteration += 1
        tts_service.say("Touch my head when you are ready.......")

        raw_input("Press enter in the terminal to take a photo in this demo > ")

        filename = 'images/captured_image_' + str(iteration) + '.jpg'
        capture_image(filename)
        time.sleep(5) # 10

        # tts_service.say(
        #     "You are now showing the image of a {}".format(choice))
        # raw_input("What image you want to show to pepper?...\n {}".format(img_list))
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

        # pred, score = library.predict_top1(
        #     library.model, img_path, library.labels)
        # Maybe if really low score, then do not give prediction but loop and ask again
        for threshold in range_to_message.keys():
            #print(threshold, range_to_message[threshold], score)
            if threshold[0] < score * 100 < threshold[1]:
                msg = range_to_message[threshold]
        tts_service.say(msg + " {}.".format(pred))
        print("The confidence for {} is equals to {}%".format(pred, round(score*100)))

        if score*100 < 50:
            tts_service.say("Let me take a look again....")
            continue
        
        # time.sleep(2)

        msg = 'Unfortunately I have nothing interesting to say about this.'
        result = ""
        try:
            # clean_string(wiki_data[pred]))#.split("\n\n")[1]))
            # print("Before acessing wikipedia pred is ", pred)
            result = library.WIKI_DATA[pred]
        except KeyError:
            tts_service.say(msg)
        if '#redirect' in result.lower():
            tts_service.say(msg)
        elif result:
            tts_service.say("Let me tell you something about it...")
            result = clean_wiki(result)

            # voice and gestures
            # ans_service = session.service("ALAnimatedSpeech")
            # configuration = {"bodyLanguageMode":"contextual"}

            tts_service.say(result)

        
        

        # best_object = most_relevant_object(result, OBJECT_ANGLES.keys())
        angle, table_synset = OBJECT_ANGLES[best_object]
        explanation = str(round(score_table*100, 4)) # to do, do from best_object, should be a return value from most_relevant_object
        tts_service.say("Let me check which one of my objects is most similar to yours and why")
        
        # for testing
        
        motion_service.moveTo(0.0, 0.0, math.radians(90))
        motion_service.moveTo(0.0, 0.0, math.radians(- 180))
        motion_service.moveTo(0.0, 0.0, math.radians(angle + 90))
        point_at_object(ALMotion)
        if table_synset != PRED_TO_SYNSET[pred]:
            tts_service.say("Ok, I found it, the most relevant object is {}".format(best_object))
            print("The association with {} has a confidence of {}%".format(best_object, explanation))

        motion_service.moveTo(0, 0.0, math.radians(-angle))

        # this must be done with synsets, how to choose best synset
        # for the user image? just make a dict ourselves
        synset1 = wordnet.synset(PRED_TO_SYNSET[pred.lower()]) # use dict instead
        synset2 = wordnet.synset(table_synset)
        path, synsets = a_star(synset1, synset2, children_mode = children_mode)
        phrase = generate_phrase2(pred, path)

        phrase = phrase.replace("_", " ")
        phrase = re.sub("\.n\.[0-9]+", "", phrase) # otherwise get definition

        if phrase:
            tts_service.say("Let me tell you why your object and mine are connected.")
            tts_service.say(phrase)
        else:
            tts_service.say("I also have a " + pred.lower() + " on my table.")
        # print(phrase)
        # Point to the object TODO
        

        # Move back to the user after pointing

    # app.run()

    # touch sensors
    # touch_service = session.service("ALTouch")
    # sl = touch_service.getSensorList() # vector of sensor names
    # print(sl)
    # v = touch_service.getStatus()  # vector of sensor status [name, bool]
    # print(v)

    # # callback function
    # anyTouch = memory_service.subscriber("TouchChanged")
    # idAnyTouch = anyTouch.signal.connect(onTouched)
    # anyTouch.signal.disconnect(idAnyTouch)


if __name__ == "__main__":
    print(os.getenv('PEPPER_TOOLS_HOME'))
    naoqiAPI()
    # pepper_cmd_api()