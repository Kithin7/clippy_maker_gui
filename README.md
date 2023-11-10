# clippy_maker_gui.py
Python ffmpeg video clipping GUI because I'm tired of messing up in the command line and "I'm a visual person" who wanted to experience the pain of coding a GUI.
## Table of Contents
- [Installation](https://github.com/Kithin7/clippy_maker_gui/edit/main/README.md#installation)
- [To-do List](https://github.com/Kithin7/clippy_maker_gui/edit/main/README.md#to-do-list)
- [Release History](https://github.com/Kithin7/clippy_maker_gui/edit/main/README.md#realse-history)

# About 🎞️
- GUI/front end for ffmpeg-python script to make clips from video files. 
- Uses ```ffmpeg.probe``` to read metadata from the input file and do magic.
- Radiobuttons and sliders for commonly changed settings for quicker clipping!
- Customizable settings file to save your favorite settings and speed up clipping!
- Output file size estimation to reduce clipping twice to get under 25 MB for sharing on [Discord](discord.com).
## Screenshots
### This is the gui at start-up
![Screenshot of the gui at start](/gui_2.png)
### This is the gui after selecting a file (oooo, ahhhh)
![Screenshot of the gui after selecting an input file](/gui_1.png)

# Installation
download the files ```clippy_maker_gui.py``` and ```clip_script.py``` and put them in the same directory and run from there.
### Dependencies
- [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
- [RangeSlider](https://pypi.org/project/RangeSlider/)
- [ffmpeg](https://pypi.org/project/ffmpeg-python/)
- [vlc](https://pypi.org/project/python-vlc/)

# To-do List 
- improve logic to remove "update source info" button
- add codecs to ffmpeg probe
    - and then add buttons to beable to choose? might have too many options or options that conflict? idk
- improve estimated size calc

# Release History
## v2023.11.??
- 
## v2023.11.??
- release version
