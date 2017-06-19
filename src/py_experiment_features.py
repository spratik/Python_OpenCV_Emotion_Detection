"""
Mani experimenting with facial information extraction.
@purpose:      To extract all possible information from an image
               and present it in json or xml format for further processing.
@applications: 1. Enhancing the multiple object detection in Computer Vision field.
               2. Capturing a moment in the time based on the extracted information
                  and applying auto filters to enhace the image.
@Based on: <a href="http://www.paulvangent.com/2016/08/05/emotion-recognition-using-facial-landmarks/">
              Emotion Recognition using Facial Landmarks, Python, DLib and OpenCV
           </a>
"""

import cv2
import dlib
import math
import numpy as np
import datetime as dt

# No need to modify this one as it is a helper script.
__version__ = "1.0, 17/06/2017"
__author__ = "Mani Kumar D A, Paul van Gent - 2016"

# Set up some required objects
video_capture = cv2.VideoCapture(0)  # Webcam object
detector = dlib.get_frontal_face_detector()  # Face detector

# Landmark identifier. Set the filename to whatever you named the
# downloaded file
predictor = dlib.shape_predictor("..\\input\\shape_predictor_68_face_landmarks.dat")

# Constant factor to convert radians to degrees.
rad2degCnvtFactor = 180 / math.pi

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(gray)

    detections = detector(clahe_image, 1)  # Detect the faces in the image

    for k, d in enumerate(detections):  # For each detected face
        shape = predictor(clahe_image, d)  # Get coordinates

        xCoordinatesList = []
        yCoordinatesList = []

        # Store the X and Y coordinates of landmark points in two lists
        for i in range(0, 68):
            xCoordinatesList.append(shape.part(i).x)
            yCoordinatesList.append(shape.part(i).y)

        # Get the mean of both axes to determine centre of gravity
        xCoordMean = np.mean(xCoordinatesList)
        yCoordMean = np.mean(yCoordinatesList)
        
        # If x-coordinates of the set are the same, the angle is 0,
        # catch to prevent 'divide by 0' error in the function
        if xCoordinatesList[27] == xCoordinatesList[30]:
            noseBridgeAngleOffset = 0
            # radians1 = 1.5708 # 90 deg = 1.5708 rads
        else:           
            radians1 = math.atan(
                (yCoordinatesList[27] - yCoordinatesList[30]) /
                (xCoordinatesList[27] - xCoordinatesList[30]))
            # since degrees = radians * rad2degCnvtFactor
            noseBridgeAngleOffset = int(radians1 * rad2degCnvtFactor)

        if noseBridgeAngleOffset < 0:
            noseBridgeAngleOffset += 90
        else:
            noseBridgeAngleOffset -= 90
            
        # For each 68 landmark points.
        for i in range(1, 68):
            
            '''
            cv2.arrowedLine(frame, (int(xCoordMean), int(yCoordMean)), 
                            (xCoordinatesList[i], yCoordinatesList[i]),
                            (0, 0, 255), thickness=1, line_type=4,
                            shift=0, tipLength=0.05)
            '''
            '''
            cv2.circle(frame, (xCoordinatesList[i], yCoordinatesList[i]),
                       1, (0, 0, 255), thickness=2)
            cv2.putText(frame, "{}".format(i), (xCoordinatesList[i], yCoordinatesList[i]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), thickness=1)
            '''
            '''
            # For each point, draw circle with thickness = 2 on the original frame
            if i == 27 or i == 30:
                cv2.circle(frame, (xCoordinatesList[i], yCoordinatesList[i]),
                       1, (0, 255, 0), thickness=2)
                cv2.putText(frame, "P{}".format(i), (xCoordinatesList[i], yCoordinatesList[i]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), thickness=1)      
            else:
                # pass                
                cv2.circle(frame, (xCoordinatesList[i], yCoordinatesList[i]),
                       1, (0, 0, 255), thickness=2)
            '''
        # For mean coordinates.
        cv2.circle(frame, (int(xCoordMean), int(yCoordMean)), 1, (255, 0, 0), thickness=2)
        cv2.putText(frame, "mean({}, {})".format(int(xCoordMean), int(yCoordMean)), 
                    (int(xCoordMean), int(yCoordMean)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), thickness=1) 

    cv2.imshow("image", frame)  # Display the frame
    
    # Save the frame when the user presses 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        img_name = "..\\img_samples\\img_cap_{}.jpg".format(
            dt.datetime.today().strftime("%Y%m%d_%H%M%S"))
        cv2.imwrite(img_name, frame)
    
    # Exit program when the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break