const API_BASE_URL = 'http://localhost:5000/api';

// DOM elements
const messagesContainer = document.getElementById('messagesContainer');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const suggestionsContainer = document.getElementById('suggestionsContainer');
const suggestionChips = document.querySelectorAll('.suggestion-chip');

// Initialize
messageInput.focus();

// Add click handlers to suggestion chips
suggestionChips.forEach(chip => {
    chip.addEventListener('click', () => {
        const query = chip.getAttribute('data-query');
        if (query) {
            messageInput.value = query;
            sendMessage();
            hideSuggestions();
        }
    });
});

// Send message function
async function sendMessage() {
    const query = messageInput.value.trim();
    
    if (!query || sendButton.disabled) {
        return;
    }

    // Add user message to UI
    addMessage(query, 'user');
    messageInput.value = '';
    messageInput.disabled = true;
    sendButton.disabled = true;

    // Show loading indicator
    const loadingId = showLoading();

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        
        // Remove loading indicator
        removeLoading(loadingId);

        if (data.success) {
            // Add bot response with grants
            addBotMessage(data.message, data.grants, data.is_help || false);
        } else {
            // Show error message
            addBotMessage(data.message || 'An error occurred while searching for grants.', []);
        }
    } catch (error) {
        console.error('Error:', error);
        removeLoading(loadingId);
        addBotMessage('Sorry, I encountered an error. Please make sure the server is running and try again.', []);
    } finally {
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

// Hide suggestions after first message
function hideSuggestions() {
    if (suggestionsContainer) {
        suggestionsContainer.classList.add('hidden');
    }
}

// Add message to chat
function addMessage(text, sender) {
    // Hide suggestions when user sends first message
    hideSuggestions();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textP = document.createElement('p');
    textP.textContent = text;
    contentDiv.appendChild(textP);
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

// Add bot message with grants
function addBotMessage(text, grants, isHelp = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Format help message with line breaks
    if (isHelp) {
        const textDiv = document.createElement('div');
        textDiv.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                 .replace(/\n/g, '<br>')
                                 .replace(/•/g, '•');
        contentDiv.appendChild(textDiv);
    } else {
        const textP = document.createElement('p');
        textP.textContent = text;
        contentDiv.appendChild(textP);
    }
    
    // Add grants if available
    if (grants && grants.length > 0) {
        const grantsList = document.createElement('div');
        grantsList.className = 'grants-list';
        
        grants.forEach(grant => {
            const grantCard = createGrantCard(grant);
            grantsList.appendChild(grantCard);
        });
        
        contentDiv.appendChild(grantsList);
    }
    
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

// Create grant card element
function createGrantCard(grant) {
    const card = document.createElement('div');
    card.className = 'grant-card';
    
    // Title
    const title = document.createElement('h3');
    title.className = 'grant-title';
    title.textContent = grant.title;
    card.appendChild(title);
    
    // Description
    const description = document.createElement('p');
    description.className = 'grant-description';
    description.textContent = grant.description;
    card.appendChild(description);
    
    // Details
    const details = document.createElement('div');
    details.className = 'grant-details';
    
    const amount = document.createElement('span');
    amount.className = 'grant-amount';
    amount.textContent = `💰 ${grant.amount}`;
    details.appendChild(amount);
    
    const deadline = document.createElement('span');
    deadline.className = 'grant-deadline';
    deadline.textContent = `📅 Deadline: ${grant.deadline}`;
    details.appendChild(deadline);
    
    const category = document.createElement('span');
    category.className = 'grant-category';
    category.textContent = `🏷️ ${grant.category}`;
    details.appendChild(category);
    
    card.appendChild(details);
    
    // Eligibility
    if (grant.eligibility) {
        const eligibility = document.createElement('p');
        eligibility.className = 'grant-eligibility';
        eligibility.innerHTML = `<strong>Eligibility:</strong> ${grant.eligibility}`;
        card.appendChild(eligibility);
    }
    
    // Link (if available)
    if (grant.link) {
        const link = document.createElement('a');
        link.href = grant.link;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.className = 'grant-link';
        link.textContent = 'Learn More →';
        card.appendChild(link);
    }
    
    return card;
}

// Show loading indicator
function showLoading() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = 'loading-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<span></span><span></span><span></span>';
    
    contentDiv.appendChild(loadingDiv);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom();
    
    return 'loading-message';
}

// Remove loading indicator
function removeLoading(loadingId) {
    const loadingElement = document.getElementById(loadingId);
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Scroll to bottom of messages
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Event listeners
sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Auto-resize input (optional enhancement)
messageInput.addEventListener('input', function() {
    sendButton.disabled = !this.value.trim();
});

// Show suggestions again if input is cleared and no messages sent
messageInput.addEventListener('focus', function() {
    // Only show suggestions if this is the first interaction
    const userMessages = document.querySelectorAll('.user-message');
    if (userMessages.length === 0 && suggestionsContainer) {
        suggestionsContainer.classList.remove('hidden');
    }
});

