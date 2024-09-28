// 獲取今天的問題
function getQuestion() {
    fetch('/get-question') // 向後端發送請求以獲取問題
        .then(response => response.json()) // 解析 JSON 格式的回應
        .then(data => {
            document.getElementById('question').innerText = data.question; // 顯示今天的問題
        })
        .catch(error => {
            console.error('Error fetching question:', error); // 錯誤處理
        });
}

// 提交每日問題的回答
function submitQuestionAnswer() {
    let questionAnswer = document.getElementById('return').value; // 獲取回答
    
    // 如果回答為空，直接返回
    if (questionAnswer.trim() === "") {
        return;
    }

    const question_and_answer = {
        question: document.getElementById('question').innerText, // 獲取當前問題
        answer: questionAnswer // 獲取回答
    };

    // 將問題與回答存入 sessionStorage
    sessionStorage.setItem('question_and_answer', JSON.stringify(question_and_answer));

    // 跳轉到 Dairy.html
    window.location.href = "Dairy"; // 將頁面導向日記頁面
}

// 初始加載
getQuestion(); // 獲取今天的問題
