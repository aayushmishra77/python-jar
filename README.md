# Jarvis - Voice-Controlled Personal Assistant

A Python-based voice assistant that can help you with various tasks through voice commands. This assistant uses speech recognition to understand your commands and responds with synthesized speech.

## Features

- Voice-controlled interface
- Wikipedia searches
- YouTube and Google searches
- System commands (shutdown, restart, lock)
- Time and IP address queries
- Natural conversation flow

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Note: This project requires Python 3.6 or higher.

## Usage

To start the voice assistant, run:
```bash
python jarvis.py
```

The assistant will greet you based on the time of day and wait for your voice commands.

## Available Commands

Here are all the voice commands you can use:

1. **Wikipedia Searches**
   - Say: "Wikipedia [topic]"
   - Example: "Wikipedia artificial intelligence"

2. **YouTube Controls**
   - Say: "Search on YouTube [query]" to search for videos
   - Say: "Open YouTube" to open the YouTube homepage
   - Example: "Search on YouTube funny cats"

3. **Google Search**
   - Say: "Search Google [query]"
   - Example: "Search Google weather today"

4. **System Information**
   - Say: "What's the time" to know the current time
   - Say: "What's my IP address" to get your public IP address

5. **System Controls**
   - Say: "Shut down" to shut down your computer
   - Say: "Restart" to restart your computer
   - Say: "Lock" to lock your computer
   - Say: "Sleep" to exit the assistant

6. **Help**
   - Say: "Help" to see all available commands

## Requirements

- Windows OS (for SAPI5 voice engine)
- Python 3.6+
- Internet connection for speech recognition and web searches
- Microphone for voice input

## Dependencies

- pyttsx3 (text-to-speech)
- speech_recognition
- wikipedia
- requests
- webbrowser (built-in)

## Note

The voice assistant uses Google's speech recognition service, so an internet connection is required for voice command recognition.