async function handleUserInput() {
    const userInput = document.getElementById("user-input").value;
    if (userInput.trim() === "") return;

    // 在 chat-box 顯示用戶輸入
    addMessage("User", userInput);

    // 傳送請求至 Flask API
    const response = await getBotResponse(userInput);

    // 在 chat-box 顯示機器人回應
    addMessage("織夢機", response);

    // 清空輸入框
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

async function getBotResponse(userInput) {
    try {
        const response = await fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        });
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error:', error);
        return "Sorry, there was an error processing your request.";
    }
}
function back() {window.location.href = "DreamWeaverHome";}