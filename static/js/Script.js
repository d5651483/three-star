

// 提交日記
document.getElementById('diaryForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 防止表單的默認提交
    let content = document.getElementById('diaryEntry').value; // 獲取日記內容

    if (content.trim() === "") {
        alert("日記內容不能為空！"); // 如果日記內容為空，提示用戶
        return;
    }

    fetch('/add-diary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // 設定請求的內容類型
        },
        body: JSON.stringify({ content: content }) // 將日記內容轉換為 JSON 格式
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // 顯示成功訊息
        document.getElementById('diaryEntry').value = ''; // 清空日記欄位
        getDiaries(); // 刷新日記列表
    })
    .catch(error => {
        console.error('Error:', error); // 錯誤處理
    });
});

// 獲取所有日記
function getDiaries() {
    fetch('/get-diaries')
        .then(response => response.json())
        .then(data => {
            let diaryDiv = document.getElementById('diaries'); // 獲取日記顯示區域
            diaryDiv.innerHTML = ''; // 清空當前日記內容
            data.forEach(diary => {
                diaryDiv.innerHTML += `<p>${diary.content} (創建時間: ${diary.created_at})</p>`; // 顯示每條日記
            });
        })
        .catch(error => {
            console.error('Error fetching diaries:', error); // 錯誤處理
        });
}

// 初始加載
getDiaries(); // 獲取所有日記