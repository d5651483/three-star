// 定義一個函數來獲取儲存在 sessionStorage 的資料
function getData() {
    // 從 sessionStorage 中獲取 'question_and_answer' 的值
    const savedData = sessionStorage.getItem('question_and_answer');

    // 檢查是否有儲存的資料
    if (savedData) {
        // 解析 JSON 格式的資料並提取問題和答案
        const { question, answer } = JSON.parse(savedData);
        // 將問題和答案顯示在日記輸入框中
        document.getElementById('diaryEntry').value = "Question: " + question + "\nAnswer: " + answer;
    } else {
        // 如果沒有資料，顯示警告提示
        alert(savedData);
    }
};

// 調用 getData 函數以執行資料獲取
getData();
