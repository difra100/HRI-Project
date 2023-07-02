import qi
import os 
import sys


def pepperVictory(robot):
  # animazione del robot quando vince il gioco
  session = robot.service("ALMotion")

  isAbsolute = True

  jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch", "LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LWristYaw", "LHand"]
  jointValues = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07, -0.141, 0.46, -0.892, 0.8, 0.98]
  times  = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
  session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  for i in range(2):
    jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [2.7, -1.3, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6, 0.6]
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)

    jointNames = ["RElbowYaw", "LElbowYaw", "HipRoll", "HeadPitch"]
    jointValues = [1.3, -2.7, -0.07, -0.07]
    times  = [0.6, 0.6, 0.6, 0.6]
    session.angleInterpolation(jointNames, jointValues, times, isAbsolute)
  
  return

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
    pepperVictory(session)