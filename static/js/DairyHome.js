function fetchDiaries() {

  fetch('/get-diaries')

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

      dairyShower(data) ;

    })
    .catch(error => console.error('獲取日記資料失敗:', error));
}

// 將資料顯示
function dairyShower(data) {

  const diaryContainer = document.getElementById('diary-container');
  diaryContainer.innerHTML = ''; // 清空之前的內容
  
  // 按日期降序排序
  data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 使用 created_at

  data.forEach(entry => {

    const diaryEntry = document.createElement('div');
    diaryEntry.classList.add('diary-entry');

    // 取得儲存日期及星期
    const createdAt = new Date(entry.created_at); // 使用 entry.created_at
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', weekday: 'short' };
    const formattedDate = createdAt.toLocaleDateString('zh-Hant-TW', options).replace(/\//g, '/'); // 格式化為 YYYY/MM/DD

    // 檢查 answers 是否存在
    const answers = entry.answers || []; // 如果 answers 未定義，設置為空陣列

    diaryEntry.innerHTML = `
      <div class="date">${formattedDate}</div> <!-- 顯示儲存的日期 -->
      <div class="entry-title">${entry.title || '無標題'}</div> <!-- 提供默認標題 -->
      <p>${entry.content || '無內容'}</p> <!-- 提供默認內容 -->
      <div class="question-answer">最開心的事: ${answers[0] || '未回答'}</div>
      <div class="question-answer">最感激的事: ${answers[1] || '未回答'}</div>
      <div class="question-answer">做得很棒的事: ${answers[2] || '未回答'}</div>
    `;
    
    diaryContainer.appendChild(diaryEntry);

  });
}

// 當頁面加載時自動獲取日記列表
document.addEventListener('DOMContentLoaded', fetchDiaries);

// 新增日記 -> 去別的地方
function AddDiary() {window.location.href = "Dairy";}
// 點擊標題 -> 回到主頁
function BackHome() {window.location.href = "Homepage";}