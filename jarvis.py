# Voice assistant Jarvis  1.0 RELISE
import csv
from googlesearch import search
import webbrowser
import requests
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
appid = "2d6b4828375bba7cc79e48b229a83724"
city_id = 702550
s_city = "Lviv,UA"
# settings
opts = {
    "alias": ('jarvis', 'jarv', 'jarvi', 'jar', 'jerrys', 'helo jarvis', 'hello jarvis'),
    "tbr": ('say', 'what', 'please', 'open', 'find', 'create'),
    "cmds": {
        "ctime": ('what time', 'time'),
        "music": ('music', 'musik',),
        "wether": ('print whether', 'what whether', 'whether'),
        "searchYt": ('in YouTube', 'YouTube'),
        "searchGo": ('in googl', 'googl', 'google'),
        "Newfolders": ('folder', 'new folder')
    }
}
 
# functions
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
def search_in_Youtub(search_term):
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
def search_in_Google(search_term):
    url = "https://www.google.com/search?q=" + search_term
    webbrowser.get().open(url)
def get_whether():
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'uk', 'APPID': appid})
        data = res.json()
        for i in data['list']:
            print( i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'] )
    except Exception as e:
        print("Exception (forecast):", e)
        pass
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "us-Us").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            # turn to Jarvis
            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            
            # recognize and execute command
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
 
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC
def execute_cmd(cmd):
    if cmd == 'ctime':   
        now = datetime.datetime.now()
        speak("Now " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'wether':
        get_whether()
    elif cmd == 'searchYt':
        search_term = input("Enter a search query")
        search_in_Youtub(search_term=search_term)
    elif cmd == 'searchGo':
        search_term = input("Enter a search query")
        search_in_Google(search_term=search_term)
    elif cmd == 'music':
        search_tem = "https://www.youtube.com/watch?v=WNadEfGnV04"
        search_in_Google(search_term=search_tem)
    elif cmd == 'Newfolders':   
        os.mkdir(r"C:\newfolder")
    else:
        print('Command not recognized, try again!')
# Starting
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
file = open
with m as source:
    r.adjust_for_ambient_noise(source)
speak_engine = pyttsx3.init()
speak("Hello!")
speak("Jarvis listens.")
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1)