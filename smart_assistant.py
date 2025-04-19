import os
import datetime
import json
from pathlib import Path
import speech_recognition as sr
import pyttsx3
import logging
import pyautogui
import webbrowser
import wikipedia
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import OpenCV, but don't fail if it's not available
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError as e:
    logger.warning(f"OpenCV (cv2) import error: {e}")
    OPENCV_AVAILABLE = False
except Exception as e:
    logger.warning(f"OpenCV (cv2) error: {e}")
    OPENCV_AVAILABLE = False

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.engine.setProperty('rate', 150)

    def speak(self, text):
        logger.info(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            logger.info("Listening...")
            self.recognizer.pause_threshold = 1
            audio = self.recognizer.listen(source)

        try:
            logger.info("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            logger.info(f"User said: {query}")
            return query.lower()
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return None

class AIProcessor:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Define system message for the AI
        self.system_message = """You are an AI assistant that helps control a computer and provide information. 
        Respond with a JSON object containing:
        {
            "category": "command_type",
            "action": "specific_action",
            "parameters": {"query": "user_query"},
            "response": "natural language response"
        }
        
        Valid categories are:
        - youtube: For YouTube related commands
        - google_search: For Google search queries
        - google: For opening Google
        - time: For time-related queries
        - wikipedia: For information queries
        - volume_up/volume_down: For volume control
        - camera: For camera operations
        - exit: For ending the session
        - shutdown: For system shutdown
        - restart: For system restart
        - general_query: For other queries

        Keep responses concise and focused on the command categorization.
        """
        
        # Keep conversation history limited
        self.conversation_history = []
        self.max_history = 5
        self.api_retry_count = 0
        self.max_retries = 3

    def process_command(self, command):
        # First try basic command processing to save API calls
        basic_result = self._basic_command_processing(command)
        if basic_result:
            return basic_result

        # If no basic command matched, try AI processing
        try:
            if self.api_retry_count >= self.max_retries:
                logger.warning("Maximum API retries reached, falling back to basic processing")
                return self._fallback_command_processing(command)

            # Add user command to history
            self.conversation_history.append({"role": "user", "content": command})
            
            # Trim history to save tokens
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            # Get AI response with reduced tokens
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_message},
                    *self.conversation_history
                ],
                temperature=0.3,  # Reduced for more focused responses
                max_tokens=100    # Reduced token count
            )
            
            # Reset retry count on successful API call
            self.api_retry_count = 0
            
            # Process response
            ai_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            try:
                return json.loads(ai_response)
            except json.JSONDecodeError:
                logger.error("Failed to parse AI response as JSON")
                return self._fallback_command_processing(command)
                
        except Exception as e:
            logger.error(f"Error in AI processing: {e}")
            self.api_retry_count += 1
            return self._fallback_command_processing(command)

    def _basic_command_processing(self, command):
        """Process common commands without using API calls"""
        if not command:
            return None
            
        command = command.lower()
        
        # Direct command matches
        direct_commands = {
            "open youtube": {"category": "youtube", "response": "Opening YouTube"},
            "what time": {"category": "time", "response": "Here's the current time"},
            "goodbye": {"category": "exit", "response": "Goodbye! Have a great day!"},
            "exit": {"category": "exit", "response": "Goodbye! Have a great day!"},
            "volume up": {"category": "volume_up", "response": "Increasing volume"},
            "volume down": {"category": "volume_down", "response": "Decreasing volume"},
            "open camera": {"category": "camera", "response": "Opening camera"},
            "shutdown computer": {"category": "shutdown", "response": "Initiating shutdown"},
            "restart computer": {"category": "restart", "response": "Initiating restart"}
        }
        
        for cmd, response in direct_commands.items():
            if cmd in command:
                return {
                    "category": response["category"],
                    "action": response["category"],
                    "parameters": {"query": command},
                    "response": response["response"]
                }
        
        return None

    def _fallback_command_processing(self, command):
        """Fallback command processing when AI is unavailable"""
        command = command.lower()
        
        # Check for common patterns
        if "google" in command and "search" in command:
            return {
                "category": "google_search",
                "action": "search",
                "parameters": {"query": command},
                "response": f"Searching Google for your query"
            }
        elif "wiki" in command or "tell me about" in command:
            return {
                "category": "wikipedia",
                "action": "search",
                "parameters": {"query": command},
                "response": f"Looking up information about your query"
            }
        
        # Default to general query if no pattern matched
        return {
            "category": "general_query",
            "action": "respond",
            "parameters": {"query": command},
            "response": "I'll try to help you with that"
        }

class ActionHandler:
    def __init__(self, voice_engine):
        self.voice_engine = voice_engine

    def handle_command(self, action):
        if not action:
            return

        category = action["category"]
        params = action.get("parameters", {})
        query = params.get("query", "")
        response = action.get("response", "")

        # Speak the AI's response if it's not a system command
        if category not in ["volume_up", "volume_down"]:
            self.voice_engine.speak(response)

        if category == "youtube":
            webbrowser.open("https://www.youtube.com")
        
        elif category == "google":
            webbrowser.open("https://www.google.com")
        
        elif category == "google_search":
            search_query = query.replace("google search", "").replace("search google for", "").replace("google for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        
        elif category == "time":
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            self.voice_engine.speak(f"The current time is {current_time}")
        
        elif category == "wikipedia":
            try:
                clean_query = query
                for word in ["wikipedia", "wiki", "tell me about", "what is"]:
                    clean_query = clean_query.replace(word, "").strip()
                results = wikipedia.summary(clean_query, sentences=2)
                self.voice_engine.speak(results)
            except:
                self.voice_engine.speak("Sorry, I couldn't find that on Wikipedia")
        
        elif category == "volume_up":
            pyautogui.press("volumeup")
        
        elif category == "volume_down":
            pyautogui.press("volumedown")
        
        elif category == "camera":
            if not OPENCV_AVAILABLE:
                self.voice_engine.speak("Sorry, camera functionality is not available")
                return
            self.handle_camera()
        
        elif category == "shutdown":
            self.voice_engine.speak("Shutting down the computer in 5 seconds")
            os.system("shutdown /s /t 5")
        
        elif category == "restart":
            self.voice_engine.speak("Restarting the computer in 5 seconds")
            os.system("shutdown /r /t 5")

    def handle_camera(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.voice_engine.speak("Could not access the camera")
                return

            self.voice_engine.speak("Camera activated. Press ESC to exit")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                cv2.imshow('Camera Feed', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            self.voice_engine.speak("Camera deactivated")
            
        except Exception as e:
            self.voice_engine.speak("Error accessing camera")
            logger.error(f"Camera error: {e}")

class SmartAssistant:
    def __init__(self):
        self.voice_engine = VoiceEngine()
        self.speech_recognizer = SpeechRecognizer()
        self.ai_processor = AIProcessor()
        self.action_handler = ActionHandler(self.voice_engine)

    def greet(self):
        hour = datetime.datetime.now().hour
        greeting = "Good morning!" if 5 <= hour < 12 else "Good afternoon!" if hour < 18 else "Good evening!"
        self.voice_engine.speak(f"{greeting} I'm your AI assistant. How can I help you today?")

    def run(self):
        self.greet()
        
        while True:
            command = self.speech_recognizer.listen()
            if not command:
                self.voice_engine.speak("I didn't catch that. Could you please repeat?")
                continue

            # Process command through AI
            action = self.ai_processor.process_command(command)
            
            # Check for exit command
            if action and action["category"] == "exit":
                self.voice_engine.speak("Goodbye! Have a great day!")
                break

            # Handle the command
            self.action_handler.handle_command(action)

if __name__ == "__main__":
    assistant = SmartAssistant()
    assistant.run() 