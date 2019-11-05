"""main.py
this python program detects a face in an image provided by /dev/video0, recognizes it, if 
an encoding is stored already, and finally detects the emotion of the recognized face.
On recognition it sends a login/logout message to the agnoMirror module


@author: Lucas Mahler @Lugges991
"""
import sys
import cv2
import json
import time
import numpy as np
import face_recognition
import time
from keras.models import load_model
from lib.helper import print_json, send_json, json_to_file
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



video_capture = cv2.VideoCapture(0)

emotion_dict= {0:'Angry' , 5:'Sad', 4:'Neutral', 1:'Disgusted', 6:'Surprised', 2:'in Fear', 3:'Happy'}

print_json('status', 'loading emotion detection model')
# Load the emotion detection model
model = load_model('/home/pi/MM_test/modules/agnoMirror/src/data/emo_model.hdf5')

print_json('status', 'loading facial encodings')
# Load a sample picture and learn how to recognize it.
lugges_image= face_recognition.load_image_file("/home/pi/MM_test/modules/agnoMirror/src/data/test.jpg")
lugges_face_encoding = face_recognition.face_encodings(lugges_image)[0]
# Create arrays of known face encodings and their names
known_face_encodings = [lugges_face_encoding]
known_face_names = ["Lucas"]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
prev_names = []
process_this_frame = True

cnt = 0

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    try:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    except Exception as e:
        print("i")
        sys.stdout.flush()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    gray_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_RGB2GRAY)

    if cnt % 30 == 0:

        # Only process every other frame of video to save time
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        timestamp = time.time()
        
        emotions = []
        # getting the emotions to the corresponding face images
        for loc in face_locations:
            face_img = gray_frame[loc[0]:loc[3], loc[2]:loc[1]]
            try:
                face_img = cv2.resize(face_img, (48,48))
                emo = np.argmax(model.predict(np.reshape(face_img, [1, face_img.shape[0], face_img.shape[1],1])))
                emotions.append(emo)
            except Exception as e:
                print("")
                sys.stdout.flush()
        
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # if the face is not unknown, add him to the names list
            if name != "Unknown":
                face_names.append(name)



        # Display the results
        for (top, right, bottom, left), name, em in zip(face_locations, face_names, emotions):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name + " is " + str(emotion_dict[em]), (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        logins = []
        logouts = []
        
        # check if there are new logins/logouts
        for n, e in zip(face_names, emotions): 
            if n not in prev_names:
                logins.append(n)
                json_to_file(n,timestamp,str(emotion_dict[e]))


        for n in prev_names:
            if n not in face_names:
                logouts.append(n)

        # send notification to the MagicMirror module
        if len(logins) > 0:
            print_json("login", {"names": logins})

        if len(logouts) > 0:
            print_json("logout", {"names": logouts})

        prev_names = face_names
    cnt += 1

    # Display the resulting image
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
