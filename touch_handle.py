# -*- encoding: UTF-8 -*-

"""Example: Say `My {Body_part} is touched` when receiving a touch event"""

import qi
import argparse
import functools
import sys

class ReactToTouch(object):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, session):
        super(ReactToTouch, self).__init__()

    
        self.memory_service = session.service("ALMemory")
        # Connect to an Naoqi1 Event.
        self.touch = self.memory_service.subscriber("TouchChanged")
        self.id = self.touch.signal.connect(functools.partial(self.onTouched, "TouchChanged"))

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Disconnect to the event when talking,
        # to avoid repetitions
        self.touch.signal.disconnect(self.id)

        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])

        self.say(touched_bodies)

        # Reconnect again to the event
        self.id = self.touch.signal.connect(functools.partial(self.onTouched, "TouchChanged"))

    def say(self, bodies):
        if (bodies == []):
            return

        sentence = "My " + bodies[0]

        for b in bodies[1:]:
            sentence = sentence + " and my " + b

        if (len(bodies) > 1):
            sentence = sentence + " are"
        else:
            sentence = sentence + " is"
        sentence = sentence + " touched."

        self.tts.say(sentence)

