import pyttsx3
import pyautogui
import speech_recognition as sr
import time
import os

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
engine.setProperty("rate", 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold =1
        audio =r.listen(source)
    
    try:
        print("Recognizing...")
        query= r.recognize_google(audio, language ="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please....")
        return "None"
    return query

if __name__ == "__main__":
      while True:
        query =takeCommand().lower()

        if "open chrome" in query:
            img = pyautogui.locateCenterOnScreen("Screenshot1.png")
            pyautogui.doubleClick(img)
            time.sleep(1)
            pyautogui.hotkey("alt","space")
            time.sleep(1)
            pyautogui.press("x")
            time.sleep(1)
            img1 = pyautogui.locateCenterOnScreen("Screenshot2.png")
            pyautogui.click(img1)
            time.sleep(2)
            img2 =pyautogui.locateCenterOnScreen("screenshot3.png")
            pyautogui.click(img2)
            time.sleep(1)
            pyautogui.typewrite("How To Manual",0.1)
            pyautogui.press("enter")
            time.sleep(1)
            pyautogui.press("esc")  # Was unable to click the subscribe button ...maybe due to cursor misplacement
            img3 = pyautogui.locateCenterOnScreen("screenshot4.png")
            pyautogui.click(img3)

        elif "close in chrome" in query:
            os.system("taskkill /f /im chrome.exe")

