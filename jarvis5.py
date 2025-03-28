import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pywhatkit as wk
import os
import pyautogui
import cv2
import sys
import time
import random 
import operator
import requests


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
        
        elif "draw a line" in query:
            pyautogui.moveTo(x=400,y=300,duration=1)
            pyautogui.leftClick()
            pyautogui.dragRel(400,0,1)
        
        elif "draw a square" in query:
            pyautogui.moveTo(x=1000, y=300, duration=1)
            pyautogui.leftClick()
            distance=400
            pyautogui.click()
            pyautogui.dragRel(distance, 0, duration=1)
            pyautogui.dragRel(0, distance, duration=1)
            pyautogui.dragRel(-distance,0,duration=1)
            pyautogui.dragRel(0,-distance,duration=1)

        elif "red colour" in query:
            pyautogui.moveTo(x=970, y=76, duration=1)
            pyautogui.click(x=970, y=76, clicks=1, interval=0, button="left")    
        
        elif "draw a rectangular spiral" in query:
            pyautogui.moveTo(x=400, y= 300 ,duration=1)
            pyautogui.leftClick()
            distance=300
            while distance>0:
                pyautogui.dragRel(distance,0,0.1,button="left")
                distance=distance-10
                pyautogui.dragRel(0,distance,0.1,button="left")
                pyautogui.dragRel(-distance, 0,0.1, button="left")
                distance=distance-10
                pyautogui.dragRel(0, -distance, 0.1, button="left")
            
        elif "close paint" in query:
            os.system("taskkill /f /im mspaint.exe")

        elif "undo" in query:
            pyautogui.hotkey("ctrl","Z")
            

        elif "open notepad" in query:
            os.startfile("C:\\WINDOWS\\system32\\notepad.exe")
        
        elif "close notepad" in query:
            os.system("taskkill/f/im notepad.exe")
        
        
        
        elif "shutdown the system" in query:  #24
            os.system("shutdown /s /t 5")
        
        elif "restart the system" in query:  #25
            os.system("shutdown /r /t 5")
        
        elif "lock the system" in query:
            os.system("rund1132.exe powrprof.dll,SetSuspendState 0,1,0")
        
        elif "hibernate the system" in query:
            os.system("rund1132.exe powrprof.dll,SetSuspendState 0,1,0")
        
        elif "open camera" in query:
            cap=cv2.VideoCapture(0)
            while True:
                ret,img =cap.read()
                cv2.imshow("webcam",img)
                k=cv2.waitKey(50)
                if k==27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "go to sleep" in query:
            speak("Alright then, I am switching off")
            sys.exit()
        
        elif "take screenshot " in query:
            speak("tell me for the screenshot")
            name = takeCommand().lower()
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot saved")
        
        elif "calculate" in query:
            r=sr.Recognizer()
            with sr.Microphone() as source:
                speak("ready")
                print("Listening....")
                r.adjust_for_ambient_noise(source)
                audio =r.listen(source)
            my_string =r.recognize_google(audio) 
            print(my_string)
            def get_operator_fn(op):
                return{
                    "+":operator.add,
                    '-':operator.sub,
                    '*':operator.mul,
                    'divided': operator.__truediv__,
                }[op]
            def eval_binary_expr(op1,oper,op2):
                op1,op2 =int(op1),int(op2)
                return get_operator_fn(oper)(op1,op2)
            speak("your result is")
            speak(eval_binary_expr(*(my_string.split())))
        
        elif "what is my ip address" in query:
            speak("checking")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                print("your ip address is")
                speak(ipAdd)
            except Exception as e :
                speak("Network is weak, please try again some time later")   

        elif "volume up" in query:
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')
            pyautogui.press('volumeup')

        elif "volume down" in query:
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")
            pyautogui.press("volumedown")

        elif "mute volume" or "unmute" in query:
            pyautogui.press("volumemute")

        elif "subscribe" in query:
            print("Everyone who are watching this video, please subscribe to our channel 'How to Manual' for interesting tutorials and information ")
            speak("Everyone who are watching this video, please subscribe to our channel 'How to Manual' for interesting tutorials and information ")
            pyautogui.hotkey("win")
            time.sleep(1)
            speak("Open your browser")
            pyautogui.typewrite("chrome",0.1)
            time.sleep(1)
            pyautogui.press("enter")
            time.sleep(1)
            speak("type youtube.com")
            pyautogui.typewrite("youtube.com",0.1)
            time.sleep(1)
            speak("press Enter")
            pyautogui.press("enter")
            speak("Click on the search bar")
            pyautogui.moveTo(806,125,1)
            pyautogui.click(806,125,1,interval=0,button="left")
            speak("type channel name")
            pyautogui.typewrite("7clouds",0.1)
            time.sleep(1)
            speak("Press Enter")
            pyautogui.press("enter")
            pyautogui.moveTo(971,314,1)
            speak("Here you will see our channel")
            pyautogui.moveTo(1688,314,1)
            speak("Click here to subscribe")
            speak("If you do not see our channel here, click on filter")
            pyautogui.moveTo(490,201,1)
            pyautogui.click(490,201,1,0,"left",)
            speak("Now click on channel")
            pyautogui.moveTo(712,361,1)
            pyautogui.click(712,361,1,0,"left")
            pyautogui.moveTo(971,314,1)
            speak("Here you will surely see our channel")
            pyautogui.moveTo(1688,314,1)
            speak("Click here to subscribe to our channel")
            pyautogui.click(1688,314,1,0,"left")




        




