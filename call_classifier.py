import os

def classify_image(image_path):
    stream = os.popen('python3 classify_image3.py hello')
    output = stream.read()
    print(locals())
    print("Outpout is")
    print(output)