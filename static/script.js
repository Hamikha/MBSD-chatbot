function appendMessage(user, message) {
    const chatBox = document.getElementById('chat-box');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', user);

    const messageContent = document.createElement('div');
    messageContent.classList.add('message');
    messageContent.textContent = message;

    messageDiv.appendChild(messageContent);
    chatBox.appendChild(messageDiv);

    chatBox.scrollTop = chatBox.scrollHeight;
}

function showThinking() {
    const chatBox = document.getElementById('chat-box');
    const thinkingDiv = document.createElement('div');
    thinkingDiv.classList.add('thinking');
    thinkingDiv.id = 'thinking-indicator';
    thinkingDiv.textContent = 'Assistant is thinking...';
    chatBox.appendChild(thinkingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function hideThinking() {
    const thinkingDiv = document.getElementById('thinking-indicator');
    if (thinkingDiv) {
        thinkingDiv.remove();
    }
}

function sendQuery() {
    const queryInput = document.getElementById('query');
    const query = queryInput.value.trim();

    if (query === "") return;

    // Append user query
    appendMessage('user', query);

    // Clear input field
    queryInput.value = '';

    // Show thinking indicator
    showThinking();

    // Send the query to FastAPI backend
    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: query }),
    })
    .then(response => response.json())
    .then(data => {
        // Hide thinking indicator
        hideThinking();

        // Append assistant's response
        appendMessage('assistant', data.answer);
    })
    .catch(error => {
        hideThinking();
        console.error('Error:', error);
    });
}

function handleEnter(event) {
    if (event.key === 'Enter') {
        sendQuery();
    }
}
