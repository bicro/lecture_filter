from pytube import YouTube
from subprocess import call
from sys import argv
import os

fname = "links.txt"

def setup():
    if not os.path.exists('lectures/'):
        os.makedirs('lectures/')
    if not os.path.exists('tmp/'):
        os.makedirs('tmp/')
    if not os.path.exists('cleaned_lectures/'):
        os.makedirs('cleaned_lectures/')

def cleanup():
    if "temp.mp3" in os.listdir("tmp"):
        os.remove("tmp/temp.mp3")
    if "temp1.mp3" in os.listdir("tmp"):
        os.remove("tmp/temp1.mp3")

def main():

    setup()
    cleanup()

    #Phase 1: Download all youtube videos specified in the "links.txt" file
    with open(fname) as f:
        lecture_links = f.readlines()
        for link in lecture_links:
            yt = YouTube(link)
            video = yt.filter('mp4')[-1]
            print yt.filename + ".mp4"
            if yt.filename + ".mp4" in os.listdir('lectures'):
                print "Skipping Download"
                continue
            print "starting - " + str(video) + str(yt.filename)
            video.download('lectures/')
            print "done download"

    #Phase 2: Clean each video using a lowpass filter and ffmpeg magic
    for filename in os.listdir('lectures'):
        if filename.endswith('.mp4'):
            #check if file has already been converted
            if filename in os.listdir('cleaned_lectures'):
                print "Skipping Conversion"
                continue

            filename = filename[:-4]
            call(["ffmpeg", "-i", "lectures/" + filename + ".mp4", "tmp/temp.mp3"])
            print "done conversion to mp3"
            call(["ffmpeg", "-i", "tmp/temp.mp3","-af","lowpass=f=6000", "tmp/temp1.mp3"])
            print "done low pass filtering mp3"
            call(["ffmpeg", "-i", "lectures/" + filename + ".mp4", "-i", "tmp/temp1.mp3", "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", "-map", "0:v:0", "-map", "1:a:0", "cleaned_lectures/" + filename + ".mp4"])
            print "done merging with original"

            #cleanup
            cleanup()

            print "done" + str(filename)

if __name__ == "__main__":
    main()
