// 獲取今天的問題
function getQuestion() {
    fetch('/get-question')
        .then(response => response.json())
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
    
    if (questionAnswer.trim() === "") {
        return; // 如果回答為空，直接返回
    }

    const question_and_answer = {
        question:document.getElementById('question').innerText,
        anser: questionAnswer
    };
    sessionStorage.setItem('question_and_anser', JSON.stringify(question_and_answer));

    // 跳轉到 Dairy.html
    window.location.href = "Dairy"; // 將頁面導向日記頁面
}

// 初始加載
getQuestion(); // 獲取今天的問題