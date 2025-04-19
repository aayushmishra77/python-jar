from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import jarvis
import datetime
import wikipedia

app = Flask(__name__)
CORS(app)

assistant = jarvis.VoiceAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get('command', '').lower()
    
    try:
        response = None
        should_exit = False

        # Handle different commands
        if 'ip address' in command:
            try:
                ip = assistant.get_ip_address(command)
                response = f"Your IP address is {ip}"
            except Exception as e:
                print(f"Error getting IP: {e}", flush=True)
                response = "Sorry, I couldn't retrieve your IP address"
        
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {current_time}"
        
        elif 'wikipedia' in command:
            # Use the assistant's improved Wikipedia search method
            try:
                assistant.handle_wikipedia_query(command)
                # The assistant's method handles the speaking, so we don't need a response here
                return jsonify({
                    'success': True,
                    'response': 'Wikipedia search completed',
                    'should_exit': False
                })
            except Exception as e:
                print(f"Wikipedia error: {e}", flush=True)
                response = "Sorry, I couldn't find that information on Wikipedia"
        
        elif 'help' in command:
            response = """I can help you with the following commands:
- "Wikipedia [topic]" to search Wikipedia
- "Search YouTube [query]" to search YouTube
- "Open YouTube" to open YouTube homepage
- "Search Google [query]" to search Google
- "What's the time" to know the current time
- "What's my IP address" to get your IP address
- "Shutdown" to shut down the computer
- "Restart" to restart the computer
- "Lock" to lock the computer
- "Sleep" to exit the assistant"""
        
        elif any(exit_cmd in command for exit_cmd in ['bye', 'goodbye', 'exit', 'quit', 'sleep']):
            response = "Goodbye! Have a great day!"
            should_exit = True
        
        # If no specific handler, use the default command processor
        if response is None:
            for command_key, handler in assistant.commands.items():
                if command_key in command:
                    try:
                        should_exit = handler(command)
                        response = "Command processed successfully"
                    except Exception as e:
                        print(f"Command handler error: {e}", flush=True)
                        response = f"Sorry, there was an error processing your command: {str(e)}"
                    break
            else:
                return jsonify({
                    'success': False,
                    'error': "Command not recognized"
                })

        # Speak the response in a separate try block
        if response:
            try:
                assistant.speak(response)
            except Exception as e:
                print(f"Speech synthesis error: {e}", flush=True)
                # Continue even if speech fails - the response will still be displayed

        return jsonify({
            'success': True,
            'response': response,
            'should_exit': should_exit
        })

    except Exception as e:
        error_msg = f"Error processing command: {str(e)}"
        print(error_msg, flush=True)
        return jsonify({
            'success': False,
            'error': error_msg
        })
1
if __name__ == '__main__':
    app.run(debug=True) 