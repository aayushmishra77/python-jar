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

    // Typing animation for responses
    function typeWriter(text, element, speed = 30) {
        let i = 0;
        element.textContent = '';
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }

    // Handle microphone button click
    micButton.addEventListener('click', () => {
        if (recognition) {
            startListening();
        } else {
            showError('Speech recognition is not supported in your browser.');
        }
    });

    // Handle command input submission
    commandInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const command = commandInput.value.trim();
            if (command) {
                processCommand(command);
            }
        }
    });

    // Add input animation
    commandInput.addEventListener('focus', () => {
        commandInput.parentElement.classList.add('input-focused');
    });

    commandInput.addEventListener('blur', () => {
        commandInput.parentElement.classList.remove('input-focused');
    });

    function startListening() {
        recognition.start();
        updateStatus('Listening...', 'recording');
        document.body.classList.add('listening');
        micButton.classList.add('pulsing');
    }

    recognition.onresult = (event) => {
        const command = event.results[0][0].transcript;
        commandInput.value = command;
        processCommand(command);
    };

    recognition.onend = () => {
        updateStatus('', '');
        document.body.classList.remove('listening');
        micButton.classList.remove('pulsing');
    };

    recognition.onerror = (event) => {
        showError(`Error: ${event.error}`);
        document.body.classList.remove('listening');
        micButton.classList.remove('pulsing');
    };

    function updateStatus(message, className) {
        status.textContent = message;
        status.className = className;
    }

    function showError(message) {
        addResponseEntry({
            success: false,
            error: message,
            timestamp: new Date()
        });
    }

    function addResponseEntry(data) {
        const entry = document.createElement('div');
        entry.className = 'response-entry';
        
        const timestamp = data.timestamp || new Date();
        const isError = !data.success;
        
        entry.innerHTML = `
            <div class="flex items-start">
                <i class="fas fa-${isError ? 'exclamation-circle text-red-400' : 'check-circle text-green-400'} mr-2 mt-1"></i>
                <div class="flex-1">
                    <div class="response-timestamp">${timestamp.toLocaleTimeString()}</div>
                    ${data.command ? `<div class="font-medium text-gray-200 mb-2">Command: ${data.command}</div>` : ''}
                    <div class="text-gray-300 whitespace-pre-wrap">
                        ${isError ? `<span class="text-red-400">${data.error}</span>` : data.response}
                    </div>
                    ${data.should_exit ? `
                        <div class="mt-2 text-blue-400">
                            <i class="fas fa-power-off mr-2"></i>
                            Jarvis is shutting down...
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        // Add entry with animation
        entry.style.opacity = '0';
        entry.style.transform = 'translateY(-10px)';
        responseArea.insertBefore(entry, responseArea.firstChild);
        
        // Trigger animation
        requestAnimationFrame(() => {
            entry.style.opacity = '1';
            entry.style.transform = 'translateY(0)';
        });
    }

    async function processCommand(command) {
        if (!command.trim()) return;

        updateStatus('Processing...', 'processing');

        try {
            const response = await fetch('/process_command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command }),
            });

            const data = await response.json();
            addResponseEntry({
                ...data,
                command: command,
                timestamp: new Date()
            });

        } catch (error) {
            showError(`Error processing command: ${error.message}`);
        } finally {
            updateStatus('', '');
            commandInput.value = '';
        }
    }

    // Add hover effect to command cards
    document.querySelectorAll('.command-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}); 