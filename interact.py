import library
import time
import os
import sys
import qi
import math
import random
import math
import json


pip = os.getenv('PEPPER_IP')

pport = 9559

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir + '/cmd_server')

from pepper_cmd import *
import pepper_cmd

url = "tcp://" + pip + ":" + str(pport)

with open("table_objects.json") as f:
    OBJECT_ANGLES = json.load(f)

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
    # time.sleep(1)

    tts_service.say(
        "If you show me some images i can tell you some facts about it.")
    # time.sleep(1.5)

    word2img = {'old man':    'images/grace_hopper.jpg',
                'pen': 'images/pen.webp',
                'book': 'images/book.jpg',
                'flask': 'images/flask.jpg',
                'glasses': 'images/glasses.webp'}
    img_list = list(word2img.keys())

    improve_image_msg = " please try to improve room lighting and put the object closer to the camera,"
    range_to_message = {
        (90, 100): "I am really sure that this is",
        (80, 90): "I am quite sure that this is",
        (50, 80): "I think that it is quite probable that this is",
        (30, 50): "I am a bit confused,"+improve_image_msg+"maybe this is...",
        (0, 30): "I am really confused"+improve_image_msg+"I can guess that the object is...",
    }

    n_tab_obj = len(OBJECT_ANGLES)

    for choice in img_list:
        print("choice", choice)
        tts_service.say(
            "So you have chosen {}".format(choice))
        # raw_input("What image you want to show to pepper?...\n {}".format(img_list))
        img_input = choice
        img_path = word2img[img_input]

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
        tts_service.say(msg + " {} with a score of {}%".format(pred, round(score*100)))

        tts_service.say("Let me tell you something about it....")
        # time.sleep(2)

        try:
            # clean_string(wiki_data[pred]))#.split("\n\n")[1]))
            result = library.WIKI_DATA[pred]
        except KeyError:
            print("I could not find this in the knowledge base, try something else")
            result = "I don't know"

        # voice and gestures
        # ans_service = session.service("ALAnimatedSpeech")
        # configuration = {"bodyLanguageMode":"contextual"}
        tts_service.say(result[:300])

        # best_object = most_relevant_object(result, OBJECT_ANGLES.keys())
        angle = OBJECT_ANGLES[best_object]
        explanation = str(round(score_table*100, 4)) # to do, do from best_object, should be a return value from most_relevant_object
        tts_service.say("Let me check which one of my objects is most similar to yours and why")
        motion_service.moveTo(0.0, 0.0, math.radians(90))
        motion_service.moveTo(0.0, 0.0, math.radians(- 180))
        motion_service.moveTo(0.0, 0.0, math.radians(angle + 90))
        tts_service.say("Ok, I found it, the most relevant object is {}, i am sure at the {}%".format(best_object, explanation))
        motion_service.moveTo(0, 0.0, math.radians(-angle))

        tts_service.say("Now ")
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
