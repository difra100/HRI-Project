# HRI-Project

The education of young children is fundamental to the progress of society, and it is proved that hands-on learning empowers their curiosity and improves the level of attention of the youngest. 
Since a shortage of teachers still affects many developed countries, we have thought of a Curiosity Bot that placed in several contexts (e.g., in libraries, restaurants, hospitals) can interact with children, satisfying their curiosity on everyday objects. According to this modality is possible to improve their learning capabilities.
To develop this project, we decided to rely on the Pepper robot's architecture because its physiognomy is intentionally designed to cultivate empathy with the user and foster a curiosity-driven interaction with humans.
We firmly believe that this deliberate choice aligns with the principles of the uncanny valley , effectively enhancing the user's curiosity during the interaction.


The Curiosity Bot should be placed behind a table with a few objects on it, a typical interaction with the robot can be summarized as follows:

- Pepper asks the children to show any object;
- Recognizes the object and provides a description of it;
- Connects the object shown with the most similar item on the table and formulate a logical sentence to show their connection.

This basic interaction loop is animated by an ask & reply-like conversation between the robot and the child, in order to assure a continuity between the two subjects. 
Our work takes advantage of Human-Robot Interaction (HRI) techniques to interface with the user in a natural way: moving around, pointing at objects, and giving the interlocutor a chance to interact, with the intent of generating a non-linear dialogue. On the other hand, Reasoning Agents (RA) techniques,  were used to generate the sentences that relate the object shown by the user and an object on the table. This is accomplished by automatically choosing a path to connect their synsets in the WordNet wordnet graph.

# Project structure

The implementation of this project is divided in the following files and folders:

- The file `full_interaction.py` is the main file that puts everything else together, it connects with the simulation of the robot Robot inside of Android Studio and performs the full interaction shown in the image below below and described in detail in the report.

- The file `synset_exploration.py` contains the planning code that uses A* to connect the starting synset (the synset of the object chosen by the user) to the ending synset (the synset of the objetc on the table that is most similar to the object chosen by the user) that is used in the project because of the much faster runtime compared to the PDDL solver.

- The folder `pddl` contains the `pyperplan` tool that we used to solve the pddl problem and out PDDL implementation. The folders written by us are:
- - `hri_small_example` that contains a small example of translating wordnet into pddl files, where the pddl problem, that contains the wordnet connections written in pddl language is manually written, together with the solution given by pyperplan.
- - `hri_large_example` that contains the code necessary to automatically convert the whole WordNet into a PDDL problem file, as mentioned in the report, the implementation is correct as validated by giving the correct result in many simple examples (of which you can find one in the `hri_small_example` folder) but the grounding is too slow to use it for real time human interaction when using the whole WordNet.

- The `camera_photo.py` file contains the code to take a photo with the webcam to make the demo more interactivel.

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

If you want to use your own camera for taking pictures, `capture_image(filename)` must be uncommented in `full_interaction.py`, otherwise the existing files in the `images/` folder would be considered.
# Final results
A video of our final version is available at this ![link](https://www.youtube.com/watch?v=3uj1IQTXOUQ).
