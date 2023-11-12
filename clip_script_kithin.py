# Kithin7's Method
import ffmpeg
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
