let isComposing = false;

// 監聽輸入法開始組字
document.getElementById("user-input").addEventListener("compositionstart", () => {
    isComposing = true;
});

// 監聽輸入法結束組字
document.getElementById("user-input").addEventListener("compositionend", () => {
    isComposing = false;
});

// 監聽鍵盤按鍵事件
document.getElementById("user-input").addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !isComposing) {
        handleUserInput(); // 呼叫傳送功能
    }
});

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
    messageDiv.innerHTML = `${message}`;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function getBotResponse(userInput) {
    try {
        const response = await fetch('/get-ai-response', {
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

function loadRecord() {
    const urlParams = new URLSearchParams(window.location.search);

    // 取得特定參數
    const paramValue = urlParams.get('num_table'); // 假設網址是 ?key=value

    fetch(`/get-talk-record?num_table=${paramValue}`)
        .then(response => response.json())
        .then(data => {

            console.log('Received array:', data); // 檢查收到的陣列

            data.forEach(record => {addMessage(record.author, record.content);});
        })
        .catch(error => console.error('Error:', error));

}

function back() {window.location.href = "DreamWeaverHome";}

loadRecord();
