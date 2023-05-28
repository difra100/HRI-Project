import os, sys
import qi
import math

pip = os.getenv('PEPPER_IP')
pport = 9559

pdir = os.getenv('PEPPER_TOOLS_HOME')
sys.path.append(pdir + '/cmd_server')

import pepper_cmd
from pepper_cmd import *

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
	tts_service.say("Hello world")

	# voice and gestures
	ans_service = session.service("ALAnimatedSpeech")
	configuration = {"bodyLanguageMode":"contextual"}
	ans_service.say("Hello. How are you?", configuration)
	motion_service = session.service("ALMotion")
	motion_service.moveTo(0.0, 0.0, math.pi)
	motion_service.moveTo(-3, 0.0, math.pi/2)

	# normal posture
	rp_service = session.service("ALRobotPosture")
	posture = "Crouch"
	speed = 2
	rp_service.goToPosture(posture,speed)
	app.run()
	
    

	# touch sensors
	# touch_service = session.service("ALTouch")
	# sl = touch_service.getSensorList() # vector of sensor names
	# print(sl)
	# v = touch_service.getStatus()  # vector of sensor status [name, bool]
	# print(v)


	# # callback function
	# anyTouch = memory_service.subscriber("TouchChanged")
	# idAnyTouch = anyTouch.signal.connect(onTouched)
	#anyTouch.signal.disconnect(idAnyTouch)
 

def pepper_cmd_api():
	begin() # connect to robot/simulator with IP in PEPPER_IP env variable

	# see pepper_tools/cmd_server/pepper_cmd.py
	pepper_cmd.robot.startSensorMonitor()
	pepper_cmd.robot.say("Hello World")
	
	# # start grabbing
	# pepper_cmd.robot.startFrameGrabber()


	# # Take and save picture
	# filename = "grab.png"
	# pepper_cmd.robot.saveImage(filename)


	# # stop grabbing
	# pepper_cmd.robot.stopFrameGrabber()

	pepper_cmd.robot.dance()



	end()

if __name__ == "__main__":
	print(os.getenv('PEPPER_TOOLS_HOME'))
	naoqiAPI()
	# pepper_cmd_api()
    
