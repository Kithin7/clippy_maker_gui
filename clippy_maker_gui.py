import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from RangeSlider import RangeSliderH
import random as rnd
import time
import subprocess
import ffmpeg
import pprint
import copy
import sys
import os
#os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC\plugins')
#import vlc

# hardcode default settings
defaults_ = {"Filetype": ".webm",
             "FPS": "30",
             "Resolution": "720p",
             "PlayCheck": 0,
             "ShowCheck": 1,
             "Start": 0,
             "Stop": 1}
# initialize source settings
source_ = {"Filetype": "?",
           "FPS": "?",
           "Resolution": "?",
           "Duration": "?",
           "Size": "?",
           "Bitrate": "?",
           }
# detect defaults or make settings file
try:   # check if it's there (but not if it's any good)
    with open("clip_settings.txt", 'r') as test:
        test.readline()
except:   # make settings file
    print("\n#######################################################")
    print("#          !!      !! WARNING !!      !!              #")
    print("#                                                     #")
    print("#    clip_settings.txt not detected in current dir!   #")
    print("#                                                     #")
    print("#          generating clip_settings.txt...            #")
    print("#                                                     #")
    print("#######################################################")
    # make file here
    settings_list = ['# settings file for clippy_maker_gui.py',
                     "Filetype=.webm",
                     "FPS=30",
                     "Resolution=720p",
                     "PlayCheck=0",
                     "ShowCheck=1",
                     "Start=0",
                     "Stop=1",
                     ]
    f = open("clip_settings.txt", 'x')
    f.close()
    with open("clip_settings.txt", 'a') as f:
        f.writelines('\n'.join(settings_list))
else:   # read in settings
    with open("clip_settings.txt", 'r') as settings:
        while True:
            a = settings.readline()
            if not settings.readline():
                break
            if a[0] == "#":
                continue
            else:
                defaults_.update({a[0:a.index("=")]: a[a.index("=")+1:len(a)-1]})
    # fix numerics

    print('\nsettings imported...')
    pprint.pprint(defaults_)


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def rng_clip_name():
    adj = ['cool', 'neat', 'blastin\'', 'chewy', 'dangerous', 'regal', 'magical', 'tasty', 'spicy', 'punctual', 'nasty',
           'HD', 'fast', 'zoomin\'', 'awesome', 'short', 'mini', 'big', 'hot', 'icy', 'godly', 'zootin\'', 'comical',
           'based', 'hot']
    noun = ['clip', 'vid', 'shareable', 'reel', 'tape', 'mixtape', 'resume', 'CV', 'application', 'video', 'DVD',
            'thing', 'thingy', 'clippy', 'blu-ray', 'revenge', 'read', 'mindreader', 'mind_game', 'outplay', 'beatin\'',
            'moment']
    name = adj[rnd.randint(0, len(adj) - 1)] + '_' + noun[rnd.randint(0, len(noun) - 1)]
    return name


def update_source_info():
    # read values from file and update source
    # ffmpeg probe outputs are different based on filetype input
    detect = inputfile.get()
    detect_type = ""
    for i in range(len(detect)):
        if detect[(1 + i) * (-1)] == ".":  # search backwards
            detect_type = detect[(1 + i) * (-1):]   # from '.' to end
            break  # break when found

    if detect_type == ".mp4":   # .mp4 from ShadowPlay
        source_.update({"Filetype": detect_type})
        source_.update({"FPS": str(ffmpeg.probe(inputfile.get())["streams"][0]["r_frame_rate"]
                                   [:ffmpeg.probe(inputfile.get())["streams"][0]["r_frame_rate"].index('/')])})
        source_.update({"Resolution": str(ffmpeg.probe(inputfile.get())["streams"][0]["height"]) + 'x' +
                                      str(ffmpeg.probe(inputfile.get())["streams"][0]["width"])})
        source_.update({"Duration": '00:00:'+str(round(float(ffmpeg.probe(inputfile.get())["format"]['duration'])))})
        source_.update({"Size": str(round(int(ffmpeg.probe(inputfile.get())["format"]["size"]) / 1024 / 1024, 2)) + ' MB'})
        source_.update({"Bitrate": str(
            round(int(ffmpeg.probe(inputfile.get())["format"]['bit_rate']) / 1024 / 1024, 2)) + ' Mbps'})

    if detect_type == ".mkv":   # .mkv from ShadowPlay
        source_.update({"Filetype": detect_type})
        source_.update({"FPS": str(ffmpeg.probe(inputfile.get())["streams"][0]["r_frame_rate"]
                                   [:ffmpeg.probe(inputfile.get())["streams"][0]["r_frame_rate"].index('/')])})
        source_.update({"Resolution": str(ffmpeg.probe(inputfile.get())["streams"][0]["height"]) + 'x' +
                                      str(ffmpeg.probe(inputfile.get())["streams"][0]["width"])})
        source_.update({"Duration": '00:00:'+str(round(float(ffmpeg.probe(inputfile.get())["format"]['duration'])))})
        source_.update({"Size": str(round(int(ffmpeg.probe(inputfile.get())["format"]["size"]) / 1024 / 1024, 2)) + ' MB'})
        source_.update({"Bitrate": str(
            round(int(ffmpeg.probe(inputfile.get())["format"]['bit_rate']) / 1024 / 1024, 2)) + ' Mbps'})

    # .webm output from ffmpeg script
    elif detect_type == '.webm':
        source_.update({"Filetype": detect_type})
        source_.update({"FPS": str(ffmpeg.probe(inputfile.get())["streams"][0]["avg_frame_rate"]
                                   [:ffmpeg.probe(inputfile.get())["streams"][0]["avg_frame_rate"].index('/')])})
        source_.update({"Resolution": str(ffmpeg.probe(inputfile.get())["streams"][0]["height"]) + 'x' +
                        str(ffmpeg.probe(inputfile.get())["streams"][0]["width"])})
        source_.update({"Duration": str(ffmpeg.probe(inputfile.get())["streams"][0]['tags']['DURATION']
                                        [:ffmpeg.probe(inputfile.get())["streams"][0]['tags']['DURATION'].index('.')])})
        source_.update({"Size": str(round(int(ffmpeg.probe(inputfile.get())["format"]["size"])/1024/1024, 2))+' MB'})
        source_.update({"Bitrate": str(round(int(ffmpeg.probe(inputfile.get())["format"]['bit_rate'])/1024/1024, 2))+' Mbps'})

    # unknown case
    else:
        # idk try the same as the .mp4?
        source_.update({"Filetype": detect_type})
        source_.update({"FPS": str(ffmpeg.probe(inputfile.get())["streams"][0]["r_frame_rate"])})
        source_.update({"Resolution": str(ffmpeg.probe(inputfile.get())["streams"][0]["height"]) + 'x' +
                                      str(ffmpeg.probe(inputfile.get())["streams"][0]["width"])})
        source_.update({"Duration": str(ffmpeg.probe(inputfile.get())["format"]['duration'])})
        source_.update(
            {"Size": str(round(int(ffmpeg.probe(inputfile.get())["format"]["size"]) / 1024 / 1024, 2)) + ' MB'})
        source_.update({"Bitrate": str(
            round(int(ffmpeg.probe(inputfile.get())["format"]['bit_rate']) / 1024 / 1024, 2)) + ' Mbps'})

    # fix Resolution for displaying
    if source_['Resolution'] == '720x1280':
        source_.update({"Resolution": '720p'})
    elif source_['Resolution'] == '1080x1920':
        source_.update({'Resolution': "1080p"})
    elif source_['Resolution'] == '480x640':
        source_.update({'Resolution': '480p'})
    elif source_['Resolution'] == '1440x2560':
        source_.update({'Resolution': '1440p'})

    # update all the source info box display and set the source vars (3 btns, 5 labels)
    # 3 btns
    t_btn_group[1]['text'] = 'source (' + source_['Filetype'] + ')'
    fps_btn_group[1]['text'] = 'source (' + source_['FPS'] + ')'
    res_btn_group[1]['text'] = 'source (' + source_['Resolution'] + ')'
    # 5 labels
    format_read_label['text'] = source_['Filetype']
    fps_read_label['text'] = source_['FPS'] + ' FPS'
    res_read_label['text'] = source_['Resolution']
    length_read_label['text'] = source_['Duration']
    size_read_label['text'] = source_['Size']
    bRate_read_label['text'] = source_['Bitrate']

    print('Source info updated!')
    pprint.pprint(source_)


def update_save_path():
    # use same parent folder of input path just minus the file
    for i in range(len(inputfile.get())):
        if inputfile.get()[(1+i)*(-1)] == '/':  # searching backwards
            savefile.set(inputfile.get()[0:len(inputfile.get())+(1+i)*(-1)+1]+rng_clip_name()+defaults_['Filetype'])
            break
    print('Save path updated!')


def select_file():
    filename = fd.askopenfilename(title='Select a file', initialdir='\\Videos')
    inputfile.trace('w', inputfile.set(str(filename)))
    # now update stuff
    update_save_path()
    update_source_info()
    calc_est_size()
    slider_make()


def select_folder():
    folderpath = fd.askdirectory(initialdir='\\Videos')
    savefile.trace('w', savefile.set(str(folderpath)+'/'+rng_clip_name()+defaults_['Filetype']))


def duration_update(aaa, bbb, ccc):
    try:
        hSlider.getValues()
    except NameError:
        print('no slider!')
    else:
        duration_label['text'] = f"Duration = {hSlider.getValues()[1] - hSlider.getValues()[0] : .0f} seconds"
        calc_est_size()


def calc_est_size():
    # est rates
    # 720p60 = 170 MBps      1080p60 = 375 MBps
    # 720p30 = 82 MBps       1080p30 = 190 MBps
    # bitrate = framesize * framerate = RES_ * FPS_
    # guess size = (duration from slider) * (bitrate)
    #            = (duration) * (bitrate) * (selected res / source res) * (selected fps / source fps)
    est_size = (hSlider.getValues()[1] - hSlider.getValues()[0]) * float(source_['Bitrate'][:source_['Bitrate'].index(" ")]) /8
    est_size_label['text'] = f'Est. size = {est_size: .1f} MB'


def slider_make():
    # make hSlider after selecting file and pulling source info
    global hSlider
    hSlider.forceValues([0, 1])
    hSlider = RangeSliderH(mainframe,
                           [hLeft, hRight],
                           Width=400,
                           Height=50,
                           padX=12,
                           bgColor='#f0f0f0',
                           font_family="Calibri",
                           valueSide='TOP',
                           font_size=10,
                           digit_precision='.0f',
                           step_size=1,
                           min_val=0,
                           max_val=int(source_['Duration'][0:2]*3600) + int(source_['Duration'][3:5]*60) +
                                   int(source_['Duration'][6:8]),
                           )
    hSlider.grid(column=0, row=slider_ROW, columnspan=7, sticky=("W", "E"))
    hSlider.forceValues([0, int(source_['Duration'][0:2]*3600) + int(source_['Duration'][3:5]*60) +
                         int(source_['Duration'][6:8])])


def clip_it():
    clipit_btn['state'] = 'disable'   # lock the button so only pressed once
    clipit_btn.update()   # force update to stop 'cached clicks'
    clipit_btn['text'] = 'clipping...'
    clipit_btn['bg'] = 'tomato'
    clipit_btn.update()   # force update to stop 'cached clicks'
    print('clipping...')

    # prep info for input
    type_input = str(t_btn_group[int(TY_.get())]['text'])
    fps_input = int(fps_btn_group[int(FPS_.get())]['text'])
    #res_input = str(res_btn_group[int(RES_.get()))]['text'])
    method_input = int(MET_.get())
    print(method_input)

    # call clip script based on choice
    if method_input == 1:
        ffclip_kithin(inputfile.get(),
                      savefile.get(),
                      hSlider.getValues()[0],
                      hSlider.getValues()[1]-hSlider.getValues()[0],
                      fps_input,
                      type_input[1:])
    elif method_input == 2:
        ffclip_springhalo(inputfile.get(),
                          savefile.get(),
                          hSlider.getValues()[0],
                          hSlider.getValues()[1])
    elif method_input == 3:
        mb.showerror('METHOD ERROR', 'Choose another method...', icon='error')
    else:
        mb.showerror('METHOD ERROR', 'Choose another method...', icon='error')
    clipit_btn.update()   # force update to stop 'cached clicks'

    # also do this stuff--
    name_fix = savefile.get().replace('/', '\\')
    name_path = ""
    for i in range(len(name_fix)):
        if name_fix[(1+i)*(-1)] == "\\":   # search backwards
            name_path = name_fix[:len(name_fix)+(1+i)*(-1)+1]
            break   # break when found
    if show_.get() == 1:  # open file explore containing folder
        try:
            with open(name_fix) as test_show:
                test_show.readline()
        except:
            subprocess.Popen(r'explorer /select, ' + name_path)
        else:
            subprocess.Popen(r'explorer /select, ' + name_fix)
    clipit_btn.update()  # force update to stop 'cached clicks'
    if play_.get() == 1:   # play back clip afterwards
        try:
            with open(name_fix) as test_show:
                test_show.readline()
        except:
            pass
        else:
            subprocess.Popen(r'C:\Program Files\VideoLAN\VLC\vlc.exe')
            #vlc.MediaPlayer(name_fix).play()   # needs fixing
    clipit_btn.update()  # force update to stop 'cached clicks'

    # clean up stuff
    clipit_btn['text'] = 'Clip it!'
    clipit_btn['bg'] = 'medium sea green'
    clipit_btn['state'] = 'normal'   # re-enable button
    clipit_btn.update()
    print('done!')


def ffclip_kithin(input, output, start, duration, fps, format):
    # 1 pass simple
    out = ffmpeg.output(
        ffmpeg.input(input, ss=start, t=duration),
        output,
        fpsmax=fps,
        format=format)
    out.run()


def ffclip_springhalo(filename_path, output_name, start_time, end_time):
    # 2-pass with some other features

    # version 1.2
    # patch notes:
    # added support for timestamps in MM:SS format
    # added support for downscaling to 1080p if video is bigger
    # added bitrate, filesize

    # input arguments: filename-as-full-path, output_name, start time, end time
    # output_name doesn't need file extension (webm auto-added)
    # eg. "D:\Videos\Shadowplay\Battlefield 2042\Replay 2023-08-28 18-47-14.mkv" outputname 45 54

    # bitrate is in bits, filesize is in bytes
    MAX_BITRATE = 15 * 1000000
    MAX_HEIGHT = 1080
    MAX_FILESIZE = 22 * 1000000

    def abr_vbr_1st_pass(inputPath, params):
        params.update({
            'pass': 1,
            'f': 'null'
        })
        ffInput = ffmpeg.input(inputPath)
        ffOutput = ffInput.output('pipe:', **params)
        ffOutput = ffOutput.global_args('-loglevel', 'error')
        std_out, std_err = ffOutput.run(capture_stdout=True)

        return params

    def abr_vbr_2nd_pass(inputPath, outputPath, params):
        params.update({
            'pass': 2,
            'f': 'webm'
        })
        ffInput = ffmpeg.input(inputPath)
        ffOutput = ffInput.output(
            outputPath,
            **params
        )
        ffOutput = ffOutput.global_args('-loglevel', 'error')
        ffOutput.run(overwrite_output=True)

    # set input arguments to variables for better readability
    inputPath = filename_path
    outputPath = output_name

    # convert mm:ss to seconds for later maths
    #start_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(':'))))
    #end_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(end_time.split(':'))))

    # create scaling string to scale down to max_height or the input height, whichever is smaller
    video_filters = "scale=-1:'min(" + str(MAX_HEIGHT) + ",ih)'"

    # set bitrate to 15Mbit or keep below 22MB
    bitrate = MAX_FILESIZE * 8 / (int(end_time) - int(start_time))
    if bitrate > MAX_BITRATE:
        bitrate = MAX_BITRATE

    params = {
        'ss': start_time,
        'to': end_time,
        'vf': video_filters,
        'row-mt': 1,
        'c:v': 'libvpx-vp9',
        'f': 'webm',
        'b:v': bitrate
    }

    params = abr_vbr_1st_pass(inputPath, params)
    abr_vbr_2nd_pass(inputPath, outputPath, params)


def ffclip_greenbagel():
    # under construction
    pass


# initialize gui window
root = tk.Tk()
root.title("Kithin's Clippy Maker GUI")
root.geometry("")
mainframe = tk.Frame(root)
mainframe.pack()
filename = 'D:/Videos/'
savename = 'D:/Videos/'


# create widget and then place it
# row 1 - input info
ROW = 1
t1 = tk.Label(mainframe, text="Input path: ")
t1.grid(column=0, row=ROW, sticky="E")

inputfile = tk.StringVar(mainframe, value=f'{filename}')
inputfile_widget = tk.Entry(mainframe, width=55, textvariable=inputfile, justify='left')
inputfile_widget.grid(column=1, row=ROW, columnspan=3, sticky=("W", "E"))
inputfile_widget.focus_set()

browse_btn = tk.Button(mainframe, text=" ... ", relief="raised", command=select_file)
browse_btn.grid(column=4, row=ROW)

update_btn = tk.Button(mainframe, text="update source info", relief="raised", command=update_source_info)
update_btn.grid(column=5, row=ROW, sticky=("W", "E"))

# row 2 - save info
ROW += 1
t2 = tk.Label(mainframe, text="Save path: ")
t2.grid(column=0, row=ROW, sticky="E")

savefile = tk.StringVar(mainframe, value=f'{savename}')
savefile_widget = tk.Entry(mainframe, width=55, textvariable=savefile, justify='left')
savefile_widget.grid(column=1, row=ROW, columnspan=3, sticky=("W", "E"))

browse_btn2 = tk.Button(mainframe, text=" ... ", relief="raised", command=select_folder)
browse_btn2.grid(column=4, row=ROW)

same_folder_btn = tk.Button(mainframe, text="   use same folder  ", relief="raised", command=update_save_path)
same_folder_btn.grid(column=5, row=ROW, sticky=("W", "E"))

# row 3 - separator bar
ROW += 1
sep3 = ttk.Separator(mainframe, orient="horizontal")
sep3.grid(column=0, row=ROW, columnspan=7, sticky=("W", "E"), pady=10)

# row 4 - radio buttons in groups
ROW += 1
# output type
type_label = tk.Label(mainframe, text="File Type:")
type_label.grid(row=ROW, column=0, padx=10, sticky="W")
outtext = ['Default ('+defaults_['Filetype']+')',
           'source ('+source_['Filetype']+')',
           '.webm',
           '.mp4']
TY_ = tk.StringVar(mainframe, '1')
t_btn_group = []
for i in range(len(outtext)):
    ROW += 1
    t_btn = tk.Radiobutton(mainframe, text=outtext[i], value=i+1, variable=TY_)
    t_btn.grid(row=ROW, column=0, padx=10, sticky="W")
    t_btn_group.append(t_btn)

# FPS
ROW -= len(outtext)  # reset to be on same row as other label
fps_label = tk.Label(mainframe, text="FPS:")
fps_label.grid(row=ROW, column=1, padx=10, sticky="W")
fpstext = ['Default (' + defaults_['FPS'] + ')',
           'source (' + source_['FPS'] + ')',
           '60',
           '30']
FPS_ = tk.StringVar(mainframe, '1')
fps_btn_group = []
for i in range(len(fpstext)):
    ROW += 1
    fps_btn = tk.Radiobutton(mainframe, text=fpstext[i], value=i+1, variable=FPS_)
    fps_btn.grid(row=ROW, column=1, padx=10, sticky="W")
    fps_btn_group.append(fps_btn)

# Resolution
ROW -= len(fpstext)  # reset to be on same row as other label
res_label = tk.Label(mainframe, text="Resolution:")
res_label.grid(row=ROW, column=2, padx=10, sticky="W")
restext = ['Default ('+defaults_['Resolution']+')',
           'source ('+source_['Resolution']+')',
           '1080p',
           '720p']
RES_ = tk.StringVar(mainframe, '1')
res_btn_group = []
for i in range(len(restext)):
    ROW += 1
    res_btn = tk.Radiobutton(mainframe, text=restext[i], value=i+1, variable=RES_)
    res_btn.grid(row=ROW, column=2, padx=10, sticky="W")
    res_btn_group.append(res_btn)

# Method
ROW -= len(restext)  # reset to be on same row as other label
met_label = tk.Label(mainframe, text="Method:")
met_label.grid(row=ROW, column=3, padx=10, sticky="W")
mettext = ['1-pass (fast) Kithin\'s ',
           '2-pass (quality) SpringHalo\'s ',
           '2-pass (?) GreenBagel\'s',
           'reserved']
MET_ = tk.StringVar(mainframe, '1')
met_btn_group = []
for i in range(len(mettext)):
    ROW += 1
    met_btn = tk.Radiobutton(mainframe, text=mettext[i], value=i+1, variable=MET_)
    met_btn.grid(row=ROW, column=3, padx=10, sticky="W")
    met_btn_group.append(met_btn)

# vert sep bar
ROW -= len(restext)
sep4 = ttk.Separator(mainframe, orient="vertical")
sep4.grid(column=4, row=ROW, rowspan=5, sticky=("N", "S"), padx=10)

# source info
# update based on selected input file
s_label = tk.Label(mainframe, text='Source info:')
s_label.grid(column=5, row=ROW, columnspan=2, sticky=("W", "E"))

ROW += 1
format_read_label = tk.Label(mainframe, text=source_['Filetype'])
format_read_label.grid(column=5, row=ROW, sticky='W')
length_read_label = tk.Label(mainframe, text=source_['Duration'])
length_read_label.grid(column=5, row=ROW, columnspan=2, sticky='E')

ROW += 1
fps_read_label = tk.Label(mainframe, text=source_['FPS'])
fps_read_label.grid(column=5, row=ROW, sticky='W')
bRate_read_label = tk.Label(mainframe, text=source_['Bitrate'])
bRate_read_label.grid(column=5, row=ROW, columnspan=2, sticky='E')

ROW += 1
res_read_label = tk.Label(mainframe, text=source_['Resolution'])
res_read_label.grid(column=5, row=ROW, sticky='W')
size_read_label = tk.Label(mainframe, text=source_['Size'])
size_read_label.grid(column=5, row=ROW, columnspan=2, sticky='E')
ROW += 1  # for blank row

# row 6 - separator bar
ROW += 1
sep6 = ttk.Separator(mainframe, orient="horizontal")
sep6.grid(column=0, row=ROW, columnspan=9, sticky=("W", "E"), pady=10)

# row 7 - slider for start/stop
ROW += 1
slider_ROW = copy.deepcopy(ROW)
# https://pypi.org/project/RangeSlider/
hLeft = tk.DoubleVar(value=defaults_["Start"])
hRight = tk.DoubleVar(value=defaults_["Stop"])
# hSlider   # reserved space for slider
global hSlider
hSlider = RangeSliderH(mainframe,
                       [hLeft, hRight],
                       Width=400,
                       Height=50,
                       padX=12,
                       bgColor='#f0f0f0',
                       font_family="Calibri",
                       valueSide='TOP',
                       font_size=10,
                       digit_precision='.0f',
                       step_size=1,
                       min_val=0,
                       max_val=10,
                       )
hSlider.grid(column=0, row=slider_ROW, columnspan=9, sticky=("W", "E"))
hLeft.trace_add("write", duration_update)
hRight.trace_add("write", duration_update)

# row 8 - estimations & go button & checkboxes(toggle on/off)
ROW += 1
duration_label = tk.Label(mainframe, text=f"Duration = {hSlider.getValues()[1] - hSlider.getValues()[0] : .0f} seconds")
duration_label.grid(column=0, row=ROW, sticky="W")

clipit_btn = tk.Button(mainframe, text="Clip it!", relief="raised",
                       bg="medium sea green", fg="white",
                       activebackground="tomato",
                       command=clip_it)
clipit_btn.grid(column=1, row=ROW,
                columnspan=3, rowspan=2,
                sticky=("W", "E"),
                ipady=10, ipadx=10)

play_ = tk.IntVar()
play_check = tk.Checkbutton(mainframe,
                            text='Play on completion?',
                            variable=play_,
                            offvalue=0,
                            onvalue=1)
play_check.grid(column=4, row=ROW, columnspan=2, sticky="W")
if defaults_['PlayCheck'] == 1:
    play_check.select()

# row 9
ROW += 1
est_size = 0
est_size_label = tk.Label(mainframe, text=f'Est. size = {est_size} MB')
est_size_label.grid(column=0, row=ROW, sticky="W")

show_ = tk.IntVar()
show_check = tk.Checkbutton(mainframe,
                            text='Show in folder?',
                            variable=show_,
                            offvalue=0,
                            onvalue=1)
show_check.grid(column=4, row=ROW, columnspan=2, sticky="W")
if defaults_['ShowCheck'] == 1:
    show_check.select()

center(root)
root.mainloop()
