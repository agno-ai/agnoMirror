import cv2
import numpy as np
import face_recognition
from keras.models import load_model

video_capture = cv2.VideoCapture(0)

emotion_dict= {0:'Angry' , 5:'Sad', 4:'Neutral', 1:'Disgusted', 6:'Surprised', 2:'in Fear', 3:'Happy'}

# Load the emotion detection model
model = load_model('/home/pi/MM_test/modules/agnoMirror/src/data/emo_model.hdf5')

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
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
    try:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    except Exception as e:
        print("small frame", frame.shape)
        print(str(e))
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    gray_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_RGB2GRAY)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        emotions = []
        for loc in face_locations:
            face_img = gray_frame[loc[0]:loc[3], loc[2]:loc[1]]
            try:
                face_img = cv2.resize(face_img, (48,48))
                emo = np.argmax(model.predict(np.reshape(face_img, [1, face_img.shape[0], face_img.shape[1],1])))
                emotions.append(emo)
            except Exception as e:
                print("face img", frame.shape)
                print(str(e))




        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


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

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
