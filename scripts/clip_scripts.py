# couple of ways to clip and process

# SpringHalo's Method
import ffmpeg   # pip install ffmpeg-python
import sys
import os


#version 1.2
# patch notes:
# added support for timestamps in MM:SS format
# added support for downscaling to 1080p if video is bigger
# added bitrate, filesize

# input arguments: filename-as-full-path, output_name, start time, end time
# output_name doesn't need file extension (webm auto-added)
# eg. "D:\Videos\Shadowplay\Battlefield 2042\Replay 2023-08-28 18-47-14.mkv" outputname 45 54

# bitrate is in bits, filesize is in bytes
MAX_BITRATE = 15*1000000
MAX_HEIGHT = 1080
MAX_FILESIZE = 22*1000000


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
inputPath = sys.argv[1]
outputPath = os.getcwd()+"\\"+sys.argv[2]+".webm"

# convert mm:ss to seconds for later maths
start_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(sys.argv[3].split(':'))))
end_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(sys.argv[4].split(':'))))

# create scaling string to scale down to max_height or the input height, whichever is smaller
video_filters = "scale=-1:'min("+str(MAX_HEIGHT)+",ih)'"

# set bitrate to 15Mbit or keep below 22MB
bitrate = MAX_FILESIZE*8/(int(end_time) - int(start_time))
if bitrate > MAX_BITRATE:
    bitrate = MAX_BITRATE

params =    {
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


# Kithin7's Method
#import ffmpeg
Input = input("Video filepath:  ")
Start = input("Seek to start time (MM:SS or seconds):  ")
Duration = input("Duration (MM:SS or seconds):  ")
Stream = ffmpeg.input(Input, ss=Start, t=Duration)
Fps = int(input("Output fps:  "))
Format = input("Output format (like webm):  ")
Out = ffmpeg.output(Stream, input("Output filepath:  ") + '.' + Format,  fpsmax=Fps, format=Format)

print('processing...')
Out.run()
print('done!')


