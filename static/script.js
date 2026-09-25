// ============================================
// GET HTML ELEMENTS
// ============================================

const input = document.getElementById("user-input");

const chatBox = document.getElementById("chat-box");


// ============================================
// ENTER KEY
// ============================================

input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {

        event.preventDefault();

        sendMessage();

    }

});


// ============================================
// SEND MESSAGE
// ============================================

async function sendMessage() {

    const message = input.value.trim();


    // Don't send empty messages

    if (message === "") {

        return;

    }


    // Remove welcome screen

    const welcomeScreen =
        document.getElementById("welcome-screen");

    if (welcomeScreen) {

        welcomeScreen.remove();

    }


    // Add user's message

    addMessage(message, "user");


    // Clear input

    input.value = "";


    // Disable send button

    const sendButton =
        document.getElementById("send-button");

    sendButton.disabled = true;


    // Show typing indicator

    showTyping();


    try {

        // Send message to Flask

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        // Check HTTP response

        if (!response.ok) {

            throw new Error(
                "Server returned " + response.status
            );

        }


        // Convert response to JSON

        const data = await response.json();


        // Remove typing indicator

        removeTyping();


        // Display AI answer

        if (data.response) {

            addMessage(
                data.response,
                "bot"
            );

        } else {

            addMessage(
                "Sorry, I didn't receive a response.",
                "bot"
            );

        }


    } catch (error) {

        console.error(
            "Chat error:",
            error
        );


        removeTyping();


        addMessage(
            "Sorry, I couldn't connect to the AI assistant. Please try again.",
            "bot"
        );

    }


    // Enable send button again

    sendButton.disabled = false;


    // Focus input

    input.focus();

}


// ============================================
// ADD MESSAGE
// ============================================

function addMessage(text, type) {


    const message =
        document.createElement("div");


    // User or bot class

    if (type === "user") {

        message.className =
            "message user-message";

    } else {

        message.className =
            "message bot-message";

    }


    // Message content

    const content =
        document.createElement("div");


    content.className =
        "message-content";


    // Put text inside message

    content.textContent = text;


    // Add content to message

    message.appendChild(content);


    // Add message to chat

    chatBox.appendChild(message);


    // Scroll down

    scrollToBottom();

}


// ============================================
// SUGGESTED QUESTIONS
// ============================================

function askQuestion(question) {


    // Put question into input

    input.value = question;


    // Automatically send it

    sendMessage();

}


// ============================================
// TYPING INDICATOR
// ============================================

function showTyping() {


    // Don't create duplicate typing indicators

    if (document.getElementById("typing")) {

        return;

    }


    const typing =
        document.createElement("div");


    typing.id = "typing";


    typing.className =
        "message bot-message";


    typing.innerHTML = `

        <div class="message-content">

            <span class="typing-text">
                Assistant is typing
            </span>

            <span class="typing-dots">
                ...
            </span>

        </div>

    `;


    chatBox.appendChild(typing);


    scrollToBottom();

}


// ============================================
// REMOVE TYPING
// ============================================

function removeTyping() {


    const typing =
        document.getElementById("typing");


    if (typing) {

        typing.remove();

    }

}


// ============================================
// NEW CHAT
// ============================================

function newChat() {

    // Clear conversation

    chatBox.innerHTML = "";


    // Create welcome screen again

    const welcome =
        document.createElement("div");


    welcome.id =
        "welcome-screen";


    welcome.innerHTML = `

        <div class="welcome-icon">
            🤖
        </div>

        <h2>
            Good afternoon 👋
        </h2>

        <p>
            How can I help you today?
        </p>

        <div class="suggestions">

            <button
                class="suggestion-card"
                onclick="askQuestion('How can I open a bank account?')"
            >

                <span class="suggestion-icon">
                    🏦
                </span>

                <div>

                    <strong>
                        Open an Account
                    </strong>

                    <small>
                        Learn about account requirements
                    </small>

                </div>

            </button>


            <button
                class="suggestion-card"
                onclick="askQuestion('What types of cards are available?')"
            >

                <span class="suggestion-icon">
                    💳
                </span>

                <div>

                    <strong>
                        Explore Cards
                    </strong>

                    <small>
                        Find the right card for you
                    </small>

                </div>

            </button>


            <button
                class="suggestion-card"
                onclick="askQuestion('What types of loans are available?')"
            >

                <span class="suggestion-icon">
                    💰
                </span>

                <div>

                    <strong>
                        Loan Services
                    </strong>

                    <small>
                        Explore available loan options
                    </small>

                </div>

            </button>


            <button
                class="suggestion-card"
                onclick="askQuestion('What digital banking services are available?')"
            >

                <span class="suggestion-icon">
                    📱
                </span>

                <div>

                    <strong>
                        Digital Banking
                    </strong>

                    <small>
                        Discover digital services
                    </small>

                </div>

            </button>

        </div>

    `;


    chatBox.appendChild(welcome);


    input.value = "";


    input.focus();

}


// ============================================
// SCROLL TO BOTTOM
// ============================================

function scrollToBottom() {


    const chatArea =
        document.querySelector(".chat-area");


    if (chatArea) {

        chatArea.scrollTop =
            chatArea.scrollHeight;

    }

}