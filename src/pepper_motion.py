"""
Implements the motion that accompanies the speech of Pepper and
the pointing motion towards the correct object.
"""

import qi
import os 
import sys

def point_at_object(motion):
    

    names = ["RShoulderPitch", "HeadPitch"]
    times = [1.0, 1.0]
    keys = [0.2, 0.2]

    motion.angleInterpolation(names, keys, times, True)
def pepperGreeting(robot):
  # animazione del robot quando vince il gioco
  session = robot.service("ALMotion")

  isAbsolute = True

  jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
  jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
  times  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
  session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  for i in range(2):
    jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [2.7, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6]
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [1.3, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6]
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  return
def pepperTalk(robot, n_hands = 2):
  # animazione del robot quando vince il gioco
  session = robot.service("ALMotion")

  isAbsolute = True

  jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", 
                "RHand", "HipRoll", "HeadPitch"]
  jointValues = [0.5, -0.46, 0.892, 1.5, 0.98, -0.07, -0.07]
  times  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
  times = [time*0.7 for time in times]
  if n_hands == 2:
     jointNames += ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
     jointValues += [0.5, 0.46, -0.892, -1.5, 0.98]
     times += [0.7 for i in range(5)]

  session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]#, "LElbowYaw"]
  jointValues = [2.7, -0.07, -0.07]#, -2.7]
  times  = [0.6, 0.6, 0.6]#, 0.6]

  if n_hands == 2:
     jointNames.append("LElbowYaw")
     jointValues.append(-2.7)
     times.append(0.6)

def pepperConfused(robot, n_hands = 2):
  # animazione del robot quando vince il gioco
  session = robot.service("ALMotion")

  isAbsolute = True

  jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", 
                "RHand", "HipRoll", "HeadPitch"]
  jointValues = [-0.4, -0.46, 0.892, 1.5, 0.98, -0.07, -0.07]
  times  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
  times = [time*0.7 for time in times]
  if n_hands == 2:
     jointNames += ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
     jointValues += [-0.4, 0.46, -0.892, -1.5, 0.98]
     times += [1 for i in range(5)]

  session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]#, "LElbowYaw"]
  jointValues = [2, -0.07, -0.07]#, -2.7]
  times  = [0.3, 0.3, 0.3]#, 0.6]

  if n_hands == 2:
     jointNames.append("LElbowYaw")
     jointValues.append(-2)
     times.append(0.3)



  session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    # jointNames = ["RElbowYaw", "HipRoll", "HeadPitch", "LElbowYaw"]
    # jointValues = [1.3, -0.07, -0.07]
    # times  = [0.6, 0.6, 0.6]
    # session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  return

def move_and_say(text, robot, service, configuration, motion):
  
  if motion == 0:
     pepperGreeting(robot)
  elif motion == 2:
     pepperTalk(robot)
  elif motion == 1:
     pepperTalk(robot, n_hands = 1)
  elif motion == 3:
     pepperConfused(robot, n_hands = 2)

  service.say(text, configuration)
   

if __name__ == '__main__':
    
    
    pip = os.getenv('PEPPER_IP')

    pport = 9559

    pdir = os.getenv('PEPPER_TOOLS_HOME')
    sys.path.append(pdir + '/cmd_server')


    from pepper_cmd import *
    import pepper_cmd

    url = "tcp://" + pip + ":" + str(pport)

    app = qi.Application(["App", "--qi-url=" + url])
    app.start()
    session = app.session
    
   
    # ALMotion = session.service("ALMotion")
    # pepperGreeting(session)
    # point_at_object(ALMotion)
    pepperConfused(session, n_hands = 2)
