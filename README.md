# lecture_filter
I made this because of incredibly annoying high pitch noises in lecture videos for CS186. It downloads the requested YouTube videos and applies a low pass filter.

#Dependencies
ffmpeg
>brew install ffmpeg

#Use
Paste all the YouTube urls that you wish to convert in "links.txt"

Run download.py
>python download.py

The cleaned up youtube videos will be stored in the "cleaned_lectures" directory.
