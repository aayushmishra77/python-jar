"""
Jarvis - A Voice-Controlled Personal Assistant

This module implements a voice-controlled personal assistant that can perform
various tasks like web searches, system operations, and information retrieval.
"""

# Standard library imports
import datetime
import os
import random
import sys
from typing import Optional, Dict, Callable
import time

# Third-party imports
import pyttsx3
import requests
import speech_recognition as sr
import webbrowser
import wikipedia


class VoiceAssistant:
    """A voice-controlled personal assistant with various capabilities."""

    def __init__(self):
        """Initialize the voice assistant with required settings."""
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Set up commands
            self.setup_commands()
            
            # Don't initialize speech engine here
            self.engine = None
            self.voices = None
        except Exception as e:
            print(f"Error initializing voice assistant: {e}")
            sys.exit(1)

    def setup_speech_engine(self):
        """Initialize the speech engine with required settings."""
        try:
            self.engine = pyttsx3.init('sapi5')
            self.voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', self.voices[0].id)
            self.engine.setProperty('rate', 150)
        except Exception as e:
            print(f"Error setting up speech engine: {e}")
            raise

    def setup_commands(self) -> None:
        """Set up command handlers for voice commands."""
        self.commands: Dict[str, Callable] = {
            # Information queries
            'wikipedia': self.handle_wikipedia_query,
            'time': self.tell_time,
            'ip address': self.get_ip_address,
            'help': self.show_help,
            
            # Web actions
            'search on youtube': self.handle_youtube_search,
            'open youtube': self.handle_youtube_open,
            'search google': self.handle_google_search,
            
            # System commands
            'shut down': self.handle_system_commands,
            'restart': self.handle_system_commands,
            'lock': self.handle_system_commands,
            'sleep': self.handle_system_commands,
            
            # Appreciation responses
            'thank': self.handle_appreciation,
            'nice': self.handle_appreciation,
            'good': self.handle_appreciation,
            'great': self.handle_appreciation,
            'awesome': self.handle_appreciation,
            'excellent': self.handle_appreciation,
            
            # Exit commands
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
        """
        Convert text to speech.
        
        Args:
            text: The text to be converted to speech
        """
        # Print the text first and ensure it's displayed immediately
        print(f"Assistant: {text}", flush=True)
        
        # Small delay to ensure text is visible before speech starts
        time.sleep(0.1)
        
        try:
            # Initialize a new engine instance for each speech request
            engine = None
            try:
                engine = pyttsx3.init()
                # Lower the rate for better clarity
                engine.setProperty('rate', 150)
                # Set up the voice
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)
                # Queue and run the speech
                engine.say(text)
                engine.runAndWait()
            finally:
                # Clean up the engine
                if engine:
                    try:
                        engine.stop()
                    except:
                        pass
                    finally:
                        del engine
                        
        except Exception as e:
            print(f"Error in speech synthesis: {e}", flush=True)

    def listen(self) -> Optional[str]:
        """
        Listen for voice input and convert to text.
        
        Returns:
            The recognized text or None if recognition failed
        """
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
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
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
        """
        Handle Wikipedia search queries.
        
        Args:
            query: The search query string
        """
        try:
            self.speak('Searching Wikipedia...')
            # Clean up the query by removing 'wikipedia' and extra spaces
            search_term = query.replace("wikipedia", "").strip()
            
            if not search_term:
                self.speak("What would you like to search for on Wikipedia?")
                return

            try:
                # First try direct search
                page = wikipedia.page(search_term, auto_suggest=False)
                summary = page.summary
            except wikipedia.DisambiguationError as e:
                # If we get a disambiguation page, take the first option
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    summary = page.summary
                    self.speak(f"Found multiple results. Showing information about {e.options[0]}")
                except:
                    raise
            except wikipedia.PageError:
                # If direct search fails, try with auto_suggest=True
                try:
                    # Search Wikipedia for possible matches
                    search_results = wikipedia.search(search_term, results=1)
                    if search_results:
                        page = wikipedia.page(search_results[0], auto_suggest=True)
                        summary = page.summary
                        self.speak(f"Showing results for {search_results[0]}")
                    else:
                        raise wikipedia.PageError(search_term)
                except:
                    raise

            # Get first two sentences of the summary
            sentences = summary.split('. ')
            short_summary = '. '.join(sentences[:2]) + '.'
            
            self.speak("According to Wikipedia:")
            print(short_summary, flush=True)
            self.speak(short_summary)
            
        except Exception as e:
            error_msg = str(e)
            print(f"Wikipedia error: {error_msg}", flush=True)
            if "Page id" in error_msg:
                self.speak("I couldn't find an exact match. Try rephrasing your search or being more specific.")
            else:
                self.speak("Sorry, I couldn't find that information on Wikipedia.")

    def handle_youtube_search(self, query: str) -> None:
        """
        Handle YouTube search commands.
        
        Args:
            query: The search query string
        """
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
        """
        Handle Google search commands.
        
        Args:
            query: The search query string
        """
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
        """
        Handle system-related commands.
        
        Args:
            query: The command string
            
        Returns:
            bool: True if the program should exit, False otherwise
        """
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

    def get_ip_address(self, command: str) -> str:
        """
        Get the public IP address.
        
        Args:
            command: The command string
            
        Returns:
            str: The public IP address
        """
        try:
            ip = requests.get('https://api.ipify.org').text
            return ip
        except Exception as e:
            print(f"Error getting IP address: {e}")
            return "Could not retrieve IP address"

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
        """
        Handle user appreciation with friendly responses.
        
        Args:
            query: The appreciation message
        """
        responses = [
            "Thank you! I'm happy to help!",
            "You're welcome! It's my pleasure to assist you.",
            "I appreciate your kind words!",
            "That's very kind of you to say!",
            "Thank you for the appreciation! Is there anything else I can help you with?"
        ]
        self.speak(random.choice(responses))

    def handle_goodbye(self, query: str) -> bool:
        """
        Handle goodbye messages with friendly farewell responses.
        
        Args:
            query: The goodbye message
            
        Returns:
            bool: True to signal program exit
        """
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
        self.speak(random.choice(farewell_messages))
        return True

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


def main():
    """Main entry point of the program."""
    try:
        assistant = VoiceAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()