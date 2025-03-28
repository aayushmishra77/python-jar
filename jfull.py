from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import cv2
import pywhatkit as kit
import sys
import pyautogui
import time
import operator
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Ready To Comply. What can I do for you?")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "channel analytics" in query:
            webbrowser.open("https://studio.youtube.com/channel/UCxeYbp9rU_HuIwVcuHvK0pw/analytics/tab-overview/period-default")

        elif 'search on youtube' in query:
            query = query.replace("search on youtube", "")
            webbrowser.open(f"www.youtube.com/results?search_query={query}")

        elif 'open youtube' in query:
            speak("What would you like to watch?")
            qrry = takeCommand().lower()
            kit.playonyt(f"{qrry}")

        elif 'close chrome' in query:
            os.system("taskkill /f /im chrome.exe")

        elif 'close youtube' in query:
            os.system("taskkill /f /im msedge.exe")

        elif 'open google' in query:
            speak("What should I search?")
            qry = takeCommand().lower()
            webbrowser.open(f"{qry}")

        # Additional commands truncated for brevity...

        elif "refresh" in query:
            pyautogui.moveTo(1551, 551, 2)
            pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
            pyautogui.moveTo(1620, 667, 1)
            pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')

        # More commands...

        elif "who created you" in query:
            print('I was created using Python, in Visual Studio Code.')
            speak('I was created using Python, in Visual Studio Code.')

        elif "open notepad and write my channel name" in query:
            pyautogui.hotkey('win')
            time.sleep(1)
            pyautogui.write('notepad')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.write("How To Manual", interval=0.1)

        elif "subscribe" in query:
            print("Please subscribe to the channel How To Manual for interesting tutorials and information. Thanks for watching.")
            speak("Please subscribe to the channel How To Manual for interesting tutorials and information. Thanks for watching.")

        elif "type" in query:
            query = query.replace("type", "")
            pyautogui.write(f"{query}")

        elif "close chrome" in query:
            os.system("taskkill /f /im chrome.exe")
