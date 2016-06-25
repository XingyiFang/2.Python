__author__ = 'Han'
# Location search
# NY: -74,40,-73,41
# DC: -77,38,-76,39
# SFO: -122,36,-121,38
# From DC to NY: -77,38,-73,41
# London: -0.2,51,-0.04,51.58
# Fairfax: -77.33, 38.818, -77.27, 38.874
# Hong Kong: 22.120085, 113.822530, 22.607763, 114.473469
# Macro: 22.099256, 113.517967, 22.221353, 113.610664
# Taiwan: 21.837747, 119.581893, 25.469767, 121.987899

import os, datetime,threading
from TwitterAPI import TwitterAPI

def do_every (interval, worker_func,iterations = 0):
  filename = 'NY2DC_'+ datetime.datetime.now().strftime("%y-%m-%d_%H_%M")
  if iterations != 1:
    threading.Timer (
      interval,
      do_every, [interval, worker_func,0 if iterations == 0 else iterations-1]
    ).start()
  worker_func(filename)

def downloadper30(filename__):
    now = datetime.datetime.now()
    startpath = 'D:\\python_app\\twitter\\Data'
    filename = filename__
    docfilename = open('filenames.txt', 'a')
    docfilename.write(filename+'\n')
    docpath = os.path.join(startpath, str(filename))
    doc = open(docpath, 'w')

    api = TwitterAPI('gO7QNRjYjCI6o8SUf9U73A', 'B7ts5BxTWJdouPi2NtnvTwIV9kd3rLHbzqjVFN7Rs',
                 '2231647664-Dr9wD2kVoa15Om51sbJYUQtJGWMXv2R7tNXrHDZ', 'iUGjLBUxjBziTqDVICs8zVdPATWAUgEJOYMYGxrGdfYBG')
    r = api.request('statuses/filter', {'locations':'-77,38,-73,41'})
    print now
    for item in r.get_iterator():
        doc.write(str(item)+'\n')
        #last time, run 31 minutes.
        if datetime.datetime.now() - now > datetime.timedelta(minutes = 31):
            print datetime.datetime.now()
            break
    docfilename.close()
    doc.close()
#create new file every 30 minutes (I set 50 times in this case, but you can use 'do_every(1800, downloadper30)' which means unlimited times)
#1800 means 1800 seconds = 30 minutes
do_every (1800, downloadper30, 50000)
