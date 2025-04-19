from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import jarvis

app = Flask(__name__)
CORS(app)

assistant = jarvis.VoiceAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    command = data.get('command', '')
    
    # Process the command through Jarvis
    for command_key, handler in assistant.commands.items():
        if command_key in command.lower():
            try:
                should_exit = handler(command)
                return jsonify({
                    'success': True,
                    'response': 'Command processed successfully',
                    'should_exit': should_exit
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                })
    
    return jsonify({
        'success': False,
        'error': "Command not recognized"
    })

if __name__ == '__main__':
    app.run(debug=True) 