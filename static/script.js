document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('micButton');
    const commandInput = document.getElementById('commandInput');
    const responseArea = document.getElementById('responseArea');
    const status = document.getElementById('status');
    
    let recognition;
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
    }

    // Handle microphone button click
    micButton.addEventListener('click', () => {
        if (recognition) {
            startListening();
        } else {
            alert('Speech recognition is not supported in your browser.');
        }
    });

    // Handle command input submission
    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            processCommand(commandInput.value);
        }
    });

    function startListening() {
        recognition.start();
        status.textContent = 'Listening...';
        status.className = 'recording';
        document.body.classList.add('listening');
    }

    recognition.onresult = (event) => {
        const command = event.results[0][0].transcript;
        commandInput.value = command;
        processCommand(command);
    };

    recognition.onend = () => {
        status.textContent = '';
        status.className = '';
        document.body.classList.remove('listening');
    };

    recognition.onerror = (event) => {
        status.textContent = `Error: ${event.error}`;
        status.className = '';
        document.body.classList.remove('listening');
    };

    async function processCommand(command) {
        if (!command.trim()) return;

        status.textContent = 'Processing...';
        status.className = 'processing';

        try {
            const response = await fetch('/process_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command }),
            });

            const data = await response.json();
            
            if (data.success) {
                appendResponse(`Command: ${command}\nResponse: Command processed successfully`);
                if (data.should_exit) {
                    appendResponse('Jarvis is shutting down...');
                }
            } else {
                appendResponse(`Command: ${command}\nError: ${data.error}`);
            }
        } catch (error) {
            appendResponse(`Error processing command: ${error.message}`);
        } finally {
            status.textContent = '';
            status.className = '';
            commandInput.value = '';
        }
    }

    function appendResponse(text) {
        const timestamp = new Date().toLocaleTimeString();
        const entry = document.createElement('div');
        entry.className = 'mb-2 pb-2 border-b border-gray-200';
        entry.innerHTML = `<span class="text-gray-400">[${timestamp}]</span><br>${text}`;
        responseArea.insertBefore(entry, responseArea.firstChild);
    }
}); 