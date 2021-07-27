#!/usr/bin/python3

import threading
import time
import youtube_dl
import sys

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '~/Desktop/DownloadedMusic/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

exitFlag = 0

downloaded = False

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print_time(self.name, self.counter, downloaded)
      print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
   while not downloaded:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))

class myThreadDownload (threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      download(self.name, downloaded)
      print ("Exiting " + self.name)

def download(threadName, counter):
   if exitFlag:
      threadName.exit()
   with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      filenames = sys.argv[1:]
      ydl.download(filenames)
      

# Create new threads
thread1 = myThread(1, "Elapsed Time", 1)
thread2 = myThreadDownload(2, "Downloader")

# Start new Threads
thread1.start()
thread2.start()
thread2.join()
if not thread2.is_alive():
   downloaded = True
print ("Exiting Main Thread")
