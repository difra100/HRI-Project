# HRI-Project

COPY FROM REPORT INTRODUCTION

# Project structure

The implementation of this project is divided in the following files and folders:

- The file `full_interaction.py` is the main file that puts everything else together, it connects with the simulation of the robot Robot inside of Android Studio and performs the full interaction shown in the image below below and described in detail in the report.

- The file `synset_exploration.py` contains the planning code that uses A* to connect the starting synset (the synset of the object chosen by the user) to the ending synset (the synset of the objetc on the table that is most similar to the object chosen by the user) that is used in the project because of the much faster runtime compared to the PDDL solver.

- The folder `pddl` contains the `pyperplan` tool that we used to solve the pddl problem and out PDDL implementation. The folders written by us are:
- - `hri_small_example` that contains a small example of translating wordnet into pddl files, where the pddl problem, that contains the wordnet connections written in pddl language is manually written, together with the solution given by pyperplan.
- - `hri_large_example` that contains the code necessary to automatically convert the whole WordNet into a PDDL problem file, as mentioned in the report, the implementation is correct as validated by giving the correct result in many simple examples (of which you can find one in the `hri_small_example` folder) but the grounding is too slow to use it for real time human interaction when using the whole WordNet.

- The `camera_photo` file contains the code to take a photo with the webcam to make the demo more interactivel.

- The `library.py` file contains many useful accessory functionality such as downloading the simple english Wikipedia archive the first time the code is run and using the pretrained CLIP model for image and text classification by calling the `classify_image3.py` and `classify_text3.py` files (that are written in Python 3 because of compatibility reasons). It also imports the file `utils.py` that contains other simpler and more general utility functions.

- The folder `setup_data` contains necessary information to inform the system of the possible objects that the children can show and the set-up of the table in front of the robot.

- The folders `glove_data` and `wikipedia_data` contain the extracted files of glove embeddings and simple english wikipedia respectively.

- The folder `images` contains some example images that can be useful to test the system.

# Set-up

- Activate the Pepper emulator in Android Studio
- Enter in the Docker and run `bash setup_all.sh`
- Start naoqi
- Run `cd src`
- Run `python full_interaction.py`
