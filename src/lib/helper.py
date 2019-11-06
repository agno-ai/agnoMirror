"""helper.py
helper module to take care of printing, sending, and saving jsons

@author: Lucas Mahler @Lugges991
"""
import json
import sys
import requests


def print_json(type, message):
    print(json.dumps({type: message}))
    sys.stdout.flush()

def send_json(face_name, timestamp, emotion):
    data = json.dumps({'face_id': face_name, 'timestamp': timestamp, 'emotion': emotion})
    headers = {'Content-type': 'application/json'}
    return requests.post('https://www.example.com/', data=data, headers=headers)

def json_to_file(face_name, timestamp, emotion):
    data = json.dumps({'face_id': str(face_name), 'timestamp': str(timestamp), 'emotion': str(emotion)})
    with open('./modules/agnoMirror/src/data/core_data/data_{}_{}.json'.format(face_name, timestamp), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

