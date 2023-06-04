from pepper_cmd import *
import pepper_cmd
import library
import time
import os
import sys
import qi
import math

pip = os.getenv('PEPPER_IP')
pport = 9559

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir + '/cmd_server')


url = "tcp://" + pip + ":" + str(pport)


def naoqiAPI():
    # session = qi.Session()

    # session.connect("tcp://{}:{}".format(pip, str(pport)))
    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session

    memory_service = app.session.service("ALMemory")

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
    threshold_to_message = {
        90: "I am really sure that this is",
        80: "I am quite sure that this is",
        50: "I think that it is quite probable that this is",
        30: "I am a bit confused,"+improve_image_msg+"maybe this is...",
        0: "I am really confused"+improve_image_msg+"I can guess that the object is...",
    }

    for choice in img_list:
        print("choice", choice)
        tts_service.say(
            "So you have chosen {}".format(choice))
        # raw_input("What image you want to show to pepper?...\n {}".format(img_list))
        img_input = choice
        img_path = word2img[img_input]
        pred, score = library.predict_top1(
            library.model, img_path, library.labels)
        tts_service.say(
            "Uhhh this a {}, i am sure about it with a confidence of {}%..".format(pred, score*100))

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
        tts_service.say(result[:50])

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
