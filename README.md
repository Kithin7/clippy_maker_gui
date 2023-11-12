# clippy_maker_gui.py
Python ffmpeg video clipping GUI because I'm tired of messing up in the command line and "I'm a visual person" who wanted to experience the pain of coding a GUI.
## Table of Contents
- [About](https://github.com/Kithin7/clippy_maker_gui/blob/main/README.md#about-%EF%B8%8F)
- [Installation](https://github.com/Kithin7/clippy_maker_gui/blob/main/README.md#installation)
- [To-do List](https://github.com/Kithin7/clippy_maker_gui/blob/main/README.md#to-do-list)
- [Release History](https://github.com/Kithin7/clippy_maker_gui/blob/main/README.md#release-history)

# About 🎞️
- GUI/front end for ffmpeg-python script to make clips from video files. 
- Uses ```ffmpeg.probe``` to read metadata from the input file and do magic.
- Radiobuttons (in groups) *and* a Slider -- *WOW!*
    - currently ```resolution``` does nothing
- Customizable settings file to save your favorite settings and speed up clipping!
- Output file size estimation to reduce clipping twice to get under 25 MB for sharing on [Discord](https://discord.com/download).
### Recommendations
- To record, NVidia ShadowPlay works pretty well. OBS is another solid option. Honestly, whatever floats your boat (but be mindful of bloaty programs like Overwolf).
- I've found myself really only needing to record the last 30 seconds or so, but I have ShadowPlay set to 75 seconds
    - My ShadowPlay settings: 75 sec, downscale to 720p (from 1440p), 60 fps, bitrate 25 Mbps
        - The bitrate is probably like 2-3x too high but everything looks good to me. Might be a good starting point and then working it down from there.
    - Google is also your friend: this is an article I found [https://riverside.fm/blog/video-bitrate](https://riverside.fm/blog/video-bitrate)
## Screenshots
### This is the gui at start-up
![Screenshot of the gui at start](/gui_2.png)
### This is the gui after selecting a file (oooo, ahhhh)
![Screenshot of the gui after selecting an input file](/gui_1.png)

# Installation
- download the file ```clippy_maker_gui.py```  and run it.
- (optional) download ```clip_script_<xxx>.py```, they are the individual scripts---they might need some masssaging to work (read through and make sure you give the inputs correctly).
### Dependencies
- [tkinter](https://docs.python.org/3/library/tkinter.html#module-tkinter)
- [RangeSlider](https://pypi.org/project/RangeSlider/)
- [ffmpeg](https://pypi.org/project/ffmpeg-python/)
- [vlc](https://pypi.org/project/python-vlc/)

# To-do List 
- improve logic to remove "update source info" button
- make ```resolution``` selection do something
- add codecs to ffmpeg probe
    - and then add buttons to beable to choose? might have too many options or options that conflict? idk
- improve estimated size calc

# Release History
## v2023.1?.??
- *WIP, coming soon*
  
## v2023.11.12
- release version
