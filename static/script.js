document.addEventListener('DOMContentLoaded', function(){
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const openChatButton = document.getElementById('open-chat');
    const closeChatButton = document.getElementById('close-chat');
    const chatWrapper = document.getElementById('chat-wrapper');

    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender.toLowerCase()}`;

        if (sender.toLowerCase() === 'dash') {
            messageElement.innerHTML = message;
        } else {
            const contentWrapper = document.createElement('div');
            contentWrapper.className = 'message-content';
            contentWrapper.textContent = message;
            messageElement.appendChild(contentWrapper);
        }
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    function addTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message dash typing-indicator';
        typingIndicator.textContent = 'DashBot is typing...';
        chatContainer.appendChild(typingIndicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return typingIndicator;
    }
    
    function removeTypingIndicator(indicator) {
        chatContainer.removeChild(indicator);
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage('User', message);
            userInput.value = '';
            const typingIndicator = addTypingIndicator();
            try {
                const response = await axios.post('/webhook', { message: message });
                const botReply = response.data.response;
                removeTypingIndicator(typingIndicator);
                addMessage('Dash', botReply);
            } catch (error) {
                removeTypingIndicator(typingIndicator);
                console.error('Error:', error);
                addMessage('Dash', 'Sorry, I encountered an error.');
            }
        }
    }
    
    function openChat() {
        chatWrapper.classList.remove('hidden');
        setTimeout(() => {
            chatWrapper.classList.add('visible');
        }, 10);
        openChatButton.style.display = 'none';
    }
    
    function closeChat() {
        chatWrapper.classList.remove('visible');
        setTimeout(() => {
            chatWrapper.classList.add('hidden');
        }, 10);
        openChatButton.style.display = 'block';
    }
    
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    
    openChatButton.addEventListener('click', openChat);
    closeChatButton.addEventListener('click', closeChat);
})