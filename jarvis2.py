import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import pyautogui

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Check if voices are available before setting the voice
if voices:
    engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    print(hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")    
    else:
        speak("Good Evening!")

    speak("Ready to comply. What can I do for you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing....")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")    
            return "None"
        return query

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()  # Get query before using it
        if 'jarvis' in query:
            print("Yes, Sir")
            speak("Yes, Sir")

        elif 'who are you' in query:
            print("My name is Jarvis")
            speak("My name is Jarvis")
            print("I can do anything that my creator programmed me to do")
            speak("I can do anything that my creator programmed me to do")

        elif 'who created you' in query:
            print("I don't know my His name, I have been created with Python language, in Visual Studio Code.")   
            speak("I don't know my His name, I have been created with Python language, in Visual Studio Code.")   
            
        elif "what is" in query:
            speak("Searching Wikipedia....")
            query = query.replace("what is","")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        elif "who is" in query:
            speak("Searching Wikipedia....")
            query = query.replace("what is","")
            results = wikipedia.summary(query,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        elif "just open google" in query:
            webbrowser.open("google.com")
        
        elif "open google" in query:
            speak("What should I search?")
            query=takeCommand().lower()
            webbrowser.open(f"{query}")
            results =wikipedia.summary(query,sentences=1)
            speak(results)  
        
        elif "just open youtube" in query:
            webbrowser.open('youtube.com')

        elif "open youtube" in query:
            speak("What you would like to watch")            
            query =takeCommand().lower()
            wk.playonyt(f"{query}")

        elif "search on youtube" in query:
            query = query.replace("search on youtube","")
            webbrowser.open(f"www.youtube.com/results?search_query={query}")

        elif "close system" in query:
            os.system("taskkill/f/im msedge.exe")

        elif "close chrome" in query:
            os.system("taskkill/f/im chrome.exe")
            
        elif "type" in query:
            query=query.replace("type","")        
            pyautogui.typewrite(f"{query}",0.1)
        
        elif "open paint" in query:
            os.startfile("C:\\WINDOWS\\system32\\mspaint.exe")

        elif "open notepad" in query:
            os.startfile("C:\\WINDOWS\\system32\\notepad.exe")
        
        elif "close notepad" in query:
            os.system("taskkill/f/im notepad.exe")




