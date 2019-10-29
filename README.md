# AgnoMirror -- MagicMirror Module for personal healthcare

The AgnoMirror Module for the [MagicMirror²](https://magicmirror.builders/)

## Dependencies

* [OpenCV](https://pypi.org/project/opencv-python/)
* [dlib](http://dlib.net/)
* [face_recognition](https://pypi.org/project/face_recognition/)
* [imutils](https://pypi.org/project/imutils/)
* [keras](https://pypi.org/project/Keras/)
* [tensorflow](https://pypi.org/project/tensorflow/)


## Installing AgnoMirror
```bash
cd ~/MagicMirror/modules/
git clone https://github.com/agno-ai/agnoMirror
cd agnoMirror
npm install
```

## Usage
Add an image of your face to `MagicMirror/modules/agnoMirror/src/data`.
Then add the following to `MagicMirror/config/config.js`:
```javascript
{
    module: "agnoMirror",
    position: "top_bar",    
    config: {
        text: "agnoMirror!"
    }
}
```
