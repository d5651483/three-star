function fetchQuestion() {

    fetch('/get-questions')
  
        .then(response => {

            if (!response.ok) {
                throw new Error('網路錯誤: ' + response.status); // 處理網路錯誤
            }

            return response.json();

        })

        .then(data => {

            // 檢查 data 是否為陣列
            if (!Array.isArray(data)) {
                console.error('數據格式錯誤:', data);
                return; // 如果格式不正確，終止函數執行
            }

            questionShower(data) ;

        })
        .catch(error => console.error('獲取日記資料失敗:', error));
}
  
// 將資料顯示
function questionShower(data) {

    const questionContainer = document.getElementById('question-container');
    questionContainer.innerHTML = ''; // 清空之前的內容

    // 按日期降序排序
    data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 使用 created_at

    data.forEach(entry => {

        const questionEntry = document.createElement('div');
        questionEntry.classList.add('question-entry');

        // 取得儲存日期及星期
        const createdAt = new Date(entry.created_at); // 使用 entry.created_at
        const options = { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' };
        const formattedDate = createdAt.toLocaleDateString('zh-Hant-TW', options).replace(/\//g, '/'); // 格式化為 YYYY/MM/DD

        questionEntry.innerHTML = `
        <div class="date-and-question">
        <div class="date">${formattedDate}</div> <!-- 顯示儲存的日期 -->
        <div class="question">${entry.question}</div> <!-- 顯示問題 -->
        </div>
        <div class="answer">${entry.answer}</div> <!-- 顯示回答 -->
        `;

        questionContainer.appendChild(questionEntry);

    });
}

// 當頁面加載時自動獲取日記列表
document.addEventListener('DOMContentLoaded', fetchQuestion);