// 獲取今天的問題
function getQuestion() {
    fetch('/genarate-question') // 向後端發送請求以獲取問題
        .then(response => response.json()) // 解析 JSON 格式的回應
        .then(data => {
            document.getElementById('question').innerText = data.question; // 顯示今天的問題
        })
        .catch(error => {
            console.error('Error fetching question:', error); // 錯誤處理
        });
}

// 提交每日問題的回答
async function submitQuestionAnswer() {

    let questionAnswer = document.getElementById('return').value; // 獲取回答
    
    // 如果回答為空，直接返回
    if (questionAnswer.trim() === "") {return;}

    const data = {
        'question': document.getElementById('question').innerText, // 獲取當前問題
        'answer': questionAnswer // 獲取回答
    };

    try {
        // 使用 fetch API 發送 POST 請求
        const response = await fetch('/add-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // 設置請求類型為 JSON
            },
            body: JSON.stringify(data) // 將對象轉換為 JSON 格式
        });

        if (response.ok) {
            const result = await response.json(); // 解析返回的 JSON 數據
            console.log(result); // 在控制台中輸出返回的結果
            window.location.href = "Homepage"; // 將頁面導向日記主頁面
        } else {
            alert('問題提交失敗！請重試。'); // 提交失敗的提示
        }
    } catch (error) {
        console.error('Error:', error); // 捕捉錯誤並輸出
    }
}

// 顯示即時時間
function updateTime() {
    // 取得當前時間
    const now = new Date();
    let hours = now.getHours();
    let minutes = now.getMinutes();

    // 時間格式補零
    if (hours < 10) {
        hours = '0' + hours;
    }
    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    // 顯示格式 例如: 13:14
    const currentTime = hours + ':' + minutes;

    // 更新網頁上的時間顯示
    document.getElementById('currentTime').textContent = currentTime;
}

// 顯示日期
function updateDate() {
    const dateElement = document.getElementById('currentDate');
    const date = new Date();

    const year = date.getFullYear();
    const months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];
    const month = months[date.getMonth()];
    const day = date.getDate();

    let daySuffix;
    if (day === 1 || day === 21 || day === 31) {
        daySuffix = 'st';
    } else if (day === 2 || day === 22) {
        daySuffix = 'nd';
    } else if (day === 3 || day === 23) {
        daySuffix = 'rd';
    } else {
        daySuffix = 'th';
    }

    const formattedDate = `${year} ${month} ${day}${daySuffix}`;
    dateElement.textContent = formattedDate;

    setInterval(updateTime, 1000);

    updateTime();

    getQuestion(); // 獲取今天的問題
}

window.onload = updateDate;
// 點擊標題 -> 回到主頁
function BackHome() {window.location.href = "Homepage";}