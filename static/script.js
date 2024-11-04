const apiUrl = 'https://api.openai.com/v1/chat/completions';
const apiKey = '';
const model = 'gpt-4';

async function handleUserInput() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // Add user input to chat-box
    addMessage("User", userInput);

    // SATIR Method: Construct the structured prompt
    const satirPrompt = `
        Situation: The user asks: "${userInput}".
        Attitude: Respond in an informative, engaging, and clear way.
        Thinking: The aim is to ensure the user feels informed and satisfied with the response.
        Intent: Generate a helpful and relevant answer.
        Response:
    `;

    const response = await getBotResponse(satirPrompt);

    // Add bot response to chat-box
    addMessage("Bot", response);

    // Clear input box
    document.getElementById("user-input").value = "";
}

function addMessage(sender, message) {
    const chatBox = document.getElementById("chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function getBotResponse(prompt) {
    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({
            model: model,
            messages: [{ role: "user", content: prompt }]
        })
    });

    const data = await response.json();
    if (data && data.choices && data.choices[0]) {
        return data.choices[0].message.content;
    } else {
        return "Sorry, I couldn't process your request.";
    }
}