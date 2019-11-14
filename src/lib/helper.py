"""helper.py
helper module to take care of printing, sending, and saving jsons
@author: Lucas Mahler @Lugges991
"""
import os
import sys
import json
import time
import pickle
import requests
import face_recognition
from pathlib import Path


# path = "./modules/agnoMirror/src/data/images"
path = "./src/data/images/"

def print_json(type, message):
    print(json.dumps({type: message}))
    sys.stdout.flush()

def send_json(face_name, timestamp, emotion):
    data = json.dumps({'account_id':'1', 'face_id': face_name, 'timestamp': time.ctime(int(timestamp)), 'emotion': emotion})
    headers = {'Content-type': 'application/json'}
    return requests.post('http://agno-dev.eu-central-1.elasticbeanstalk.com/api/users', data=data, headers=headers)

def json_to_file(face_name, timestamp, emotion):
    data = json.dumps({'face_id': str(face_name), 'timestamp': str(timestamp), 'emotion': str(emotion)})
    with open('./modules/agnoMirror/src/data/core_data/data_{}_{}.json'.format(face_name, timestamp), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def compute_encodings():
    """ 
    load the images according to their names in the directory hierarchy and compute their facial encodings

    returns a list of names and a list of their associated encodings
    """
    names = os.listdir(path)
    print(names)
    face_encodings = []
    for n in names:
        temp_fe = []
        for p in Path(path, n).rglob('*.jpg'):
            print(p)
            img = face_recognition.load_image_file(str(p))
            fe = face_recognition.face_encodings(img)
            temp_fe.append(fe[0])
        face_encodings.append(temp_fe)
    return names, face_encodings
            


def get_names_encodings():
    dir_index = compute_dir_index()
    if pickle.load(open("./modules/agnoMirror/src/data/images/cdi.pickle", "rb")) != dir_index:
        n, e = compute_encodings()
        pickle.dump([n,e],open('./modules/agnoMirror/src/data/images/encodings.pickle','wb'))
    else:
        if os.path.isfile('./modules/agnoMirror/src/data/images/encodings.pickle'):
            n, e = pickle.load(open("./modules/agnoMirror/src/data/images/encodings.pickle"))[0]
        else:
            n, e = compute_encodings()
            pickle.dump([n,e],open('encodings.pickle','wb'))
    return n, e

def compute_dir_index():
    """ Return a tuple containing:
    - list of files (relative to path)
    - lisf of subdirs (relative to path)
    - a dict: filepath => last 
    """
    files = []
    subdirs = []

    for root, dirs, filenames in os.walk(path):
        for subdir in dirs:
            subdirs.append(os.path.relpath(os.path.join(root, subdir), path))

        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), path))
        
    index = {}
    for f in files:
        index[f] = os.path.getmtime(os.path.join(path, files[0]))

    return dict(files=files, subdirs=subdirs, index=index)


