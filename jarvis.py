"""
Jarvis - A Voice-Controlled Personal Assistant
"""
import datetime
import os
import sys
from typing import Optional, Dict, Callable

import pyttsx3
import requests
import speech_recognition as sr
import webbrowser
import wikipedia

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with required settings."""
        try:
            self.engine = pyttsx3.init('sapi5')
            self.voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', self.voices[0].id)
            self.engine.setProperty('rate', 150)
            self.recognizer = sr.Recognizer()
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            self.setup_commands()
        except Exception as e:
            print(f"Error initializing voice assistant: {e}")
            sys.exit(1)
        
    def setup_commands(self) -> None:
        """Set up command handlers for better organization."""
        self.commands: Dict[str, Callable] = {
            'wikipedia': self.handle_wikipedia_query,
            'search on youtube': self.handle_youtube_search,
            'open youtube': self.handle_youtube_open,
            'search google': self.handle_google_search,
            'ip address': self.get_ip_address,
            'time': self.tell_time,
            'shut down': self.handle_system_commands,
            'restart': self.handle_system_commands,
            'lock': self.handle_system_commands,
            'sleep': self.handle_system_commands,
            'help': self.show_help,
            'thank': self.handle_appreciation,
            'nice': self.handle_appreciation,
            'good': self.handle_appreciation,
            'great': self.handle_appreciation,
            'awesome': self.handle_appreciation,
            'excellent': self.handle_appreciation,
            'bye': self.handle_goodbye,
            'goodbye': self.handle_goodbye,
            'see you': self.handle_goodbye,
            'see ya': self.handle_goodbye,
            'catch you later': self.handle_goodbye,
            'take care': self.handle_goodbye,
            'have a good day': self.handle_goodbye,
            'good night': self.handle_goodbye,
            'talk to you later': self.handle_goodbye,
            'i am leaving': self.handle_goodbye,
            'got to go': self.handle_goodbye,
            'gotta go': self.handle_goodbye,
            'farewell': self.handle_goodbye,
            'cya': self.handle_goodbye,
            'adios': self.handle_goodbye
        }
        
    def speak(self, text: str) -> None:
        """Convert text to speech."""
        try:
            print(f"Assistant: {text}")  # Print what the assistant is saying
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech synthesis: {e}")

    def listen(self) -> Optional[str]:
        """Listen for voice input and convert to text."""
        try:
            with sr.Microphone() as source:
                print("\nListening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Recognizing...")
                query = self.recognizer.recognize_google(audio, language='en-in')
                print(f"User said: {query}")
                return query.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None

    def greet(self) -> None:
        """Greet the user based on time of day."""
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        self.speak("I am Jarvis, your voice assistant. Say 'help' to learn what I can do.")

    def handle_wikipedia_query(self, query: str) -> None:
        """Handle Wikipedia search queries."""
        try:
            self.speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            print(results)
            self.speak(results)
        except Exception as e:
            self.speak("Sorry, I couldn't find that information on Wikipedia")
            print(f"Wikipedia error: {e}")

    def handle_youtube_search(self, query: str) -> None:
        """Handle YouTube search commands."""
        search_term = query.replace("search on youtube", "").strip()
        if not search_term:
            self.speak("What would you like to search for on YouTube?")
            search_term = self.listen()
            if not search_term:
                self.speak("Sorry, I couldn't understand what to search for")
                return
                
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
        self.speak(f"Searching YouTube for {search_term}")

    def handle_youtube_open(self, query: str) -> None:
        """Open YouTube homepage."""
        webbrowser.open("https://www.youtube.com")
        self.speak("Opening YouTube")

    def handle_google_search(self, query: str) -> None:
        """Handle Google search commands."""
        search_term = query.replace("search google", "").strip()
        if not search_term:
            self.speak("What would you like to search for on Google?")
            search_term = self.listen()
            if not search_term:
                self.speak("Sorry, I couldn't understand what to search for")
                return
                
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        self.speak(f"Searching Google for {search_term}")

    def handle_system_commands(self, query: str) -> bool:
        """Handle system-related commands. Returns True if should exit."""
        if "shut down" in query:
            self.speak("Are you sure you want to shut down the system? Say 'yes' to confirm or 'no' to cancel.")
            confirmation = self.listen()
            if confirmation and 'yes' in confirmation.lower():
                self.speak("Shutting down the system in 5 seconds")
                os.system("shutdown /s /t 5")
            else:
                self.speak("Shutdown cancelled")
        elif "restart" in query:
            self.speak("Are you sure you want to restart the system? Say 'yes' to confirm or 'no' to cancel.")
            confirmation = self.listen()
            if confirmation and 'yes' in confirmation.lower():
                self.speak("Restarting the system in 5 seconds")
                os.system("shutdown /r /t 5")
            else:
                self.speak("Restart cancelled")
        elif "lock" in query:
            self.speak("Are you sure you want to lock the system? Say 'yes' to confirm or 'no' to cancel.")
            confirmation = self.listen()
            if confirmation and 'yes' in confirmation.lower():
                self.speak("Locking the system")
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            else:
                self.speak("Lock cancelled")
        elif "sleep" in query:
            self.speak("Are you sure you want to exit? Say 'yes' to confirm or 'no' to cancel.")
            confirmation = self.listen()
            if confirmation and 'yes' in confirmation.lower():
                self.speak('Goodbye! Have a great day!')
                return True
            else:
                self.speak("Exit cancelled")
        return False

    def get_ip_address(self, query: str) -> None:
        """Get and speak the public IP address."""
        try:
            ip_address = requests.get('https://api.ipify.org').text
            print(f"IP Address: {ip_address}")
            self.speak(f"Your IP address is {ip_address}")
        except Exception as e:
            self.speak("Sorry, I couldn't retrieve your IP address")
            print(f"Error getting IP address: {e}")

    def tell_time(self, query: str) -> None:
        """Tell the current time."""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")

    def show_help(self, query: str) -> None:
        """Show available commands."""
        help_text = """
I can help you with the following commands:
- "Wikipedia [topic]" to search Wikipedia
- "Search on YouTube [query]" to search YouTube
- "Open YouTube" to open YouTube homepage
- "Search Google [query]" to search Google
- "What's the time" to know the current time
- "What's my IP address" to get your IP address
- "Shut down" to shut down the computer
- "Restart" to restart the computer
- "Lock" to lock the computer
- "Sleep" to exit the assistant
"""
        print(help_text)
        self.speak("Here are the commands I understand:")
        self.speak(help_text.replace("-", "").replace("\n", " ").strip())

    def handle_appreciation(self, query: str) -> None:
        """Handle user appreciation with friendly responses."""
        responses = [
            "Thank you! I'm happy to help!",
            "You're welcome! It's my pleasure to assist you.",
            "I appreciate your kind words!",
            "That's very kind of you to say!",
            "Thank you for the appreciation! Is there anything else I can help you with?"
        ]
        import random
        self.speak(random.choice(responses))

    def handle_goodbye(self, query: str) -> bool:
        """Handle goodbye messages with friendly farewell responses."""
        farewell_messages = [
            "Goodbye! Have a wonderful day!",
            "Take care! Looking forward to helping you again!",
            "Farewell! It was a pleasure assisting you!",
            "Bye bye! Stay amazing!",
            "Until next time! Have a great day ahead!",
            "It was great chatting with you! See you soon!",
            "Goodbye! Don't forget to call me if you need any help!",
            "Take care and stay safe! Goodbye!",
            "Have a fantastic rest of your day! Goodbye!",
            "Wishing you a great time ahead! See you later!",
            "Thanks for chatting! Have a wonderful time!",
            "Goodbye! Remember, I'm always here to help!",
            "See you next time! It's been a pleasure!"
        ]
        import random
        self.speak(random.choice(farewell_messages))
        return True  # Return True to signal the program to exit

    def run(self) -> None:
        """Main loop for the voice assistant."""
        self.greet()
        
        while True:
            query = self.listen()
            if not query:
                continue

            # Check for commands
            for command_key, handler in self.commands.items():
                if command_key in query:
                    if handler(query):  # If handler returns True, exit the program
                        return
                    break
            else:
                self.speak("I'm not sure how to help with that. Say 'help' to see what I can do.")

if __name__ == "__main__":
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)