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
    config: {
        // See 'Configuration options' for more information.
        defaultClass: "unknown",
        everyoneClass: "known"
    },
    classes: "known unknown Lucas"
    },
}
     module: 'example_module',
     position: 'top_left',
     //Set your classes here seperated by a space.
     //Shown for all users
     classes: 'known unknown'
}
```
