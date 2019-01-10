###Process data for use in app

import glob
import os

def get_data():
    tweets_data = glob.glob('C:\Users\Karolina\OneDrive - Imperial College London\Year 4\Sensing\Coursework\code\data_app\*tweets.csv') # * means all if need specific format then *.csv
    twitter = max(tweets_data, key=os.path.getctime)

    weather_data = glob.glob('C:\Users\Karolina\OneDrive - Imperial College London\Year 4\Sensing\Coursework\code\data_app\*weather.csv') # * means all if need specific format then *.csv
    weather = max(weather_data, key=os.path.getctime)

    with open(twitter) as t:
        lastT = list(t)[-1]
    with open(weather) as w:
        lastW = list(w)[-1]
    splitT=lastT.split(',')
    pos=float(splitT[1])
    tot=float(splitT[-1])
    if tot==0: #avoid diviidng by zero
        tot=1
    positivity=pos/tot

    splitW=lastW.split(',')
    press=float(splitW[2])
    temp=float(splitW[3])-273
    desc=splitW[-1]

    activities={0: 'Take a nap', 1: 'Drink tea', 2:'Have a good meal', 3:'Read a book', 4:'Clean your room', 5:'Make something', 6:'Call a friend', 7:'Do a chore',8:'Exercise',9:'Go for a walk',10:'Hang out with friends'}

    score=int(3.3*positivity+3.3*(temp/31)+3.3*(press/1030))
    rec=activities[score]
    return [positivity, press, temp, desc,rec]