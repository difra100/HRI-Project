"""
Uses the integrated webcam or a usb webcam to capture an image in real time.
Useful to make the demo more interactive.
"""
import cv2
import cv2 as cv 

def testDevice(source):
   cap = cv.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)

testDevice(0)


def capture_image(filename):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the resulting frame
        cv2.imshow('Camera View', frame)

        
        break

    # Release the webcam
    cap.release()

    # Destroy all the windows
    cv2.destroyAllWindows()

    # Save the captured image
    cv2.imwrite(filename, frame)

# Call the function to capture the image
if __name__ == "__main__":
    capture_image("../images/captured_image.jpg")
