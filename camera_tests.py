import cv2
import cv2 as cv 

def testDevice(source):
   cap = cv.VideoCapture(source) 
   if cap is None or not cap.isOpened():
       print('Warning: unable to open video source: ', source)

testDevice(0) # no printout
# testDevice(1) # prints message
# testDevice(2) # prints message
# testDevice(3) # prints message


def capture_image(filename):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # print(frame)

        # Display the resulting frame
        cv2.imshow('Camera View', frame)

        # Wait for 'q' key to exit
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release the webcam
    cap.release()

    # Destroy all the windows
    cv2.destroyAllWindows()

    # Save the captured image
    cv2.imwrite(filename, frame)

# Call the function to capture the image
if __name__ == "__main__":
    capture_image("images/captured_image.jpg")
