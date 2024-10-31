document.getElementById('diary-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // 防止表單默認提交

    const title = document.getElementById('diary-title').value;
    const content = document.getElementById('diary-content').value;
    const answers = [
        document.getElementById('question1').value,
        document.getElementById('question2').value,
        document.getElementById('question3').value
    ];
    console.log('Answers:', answers); // 打印回答

    // 創建要發送的對象
    const data = {
        "title": title,
        "content": content,
        "answers": answers
    };

    try {
        // 使用 fetch API 發送 POST 請求
        const response = await fetch('/add-diary', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // 設置請求類型為 JSON
            },
            body: JSON.stringify(data) // 將對象轉換為 JSON 格式
        });

        if (response.ok) {
            const result = await response.json(); // 解析返回的 JSON 數據
            console.log(result); // 在控制台中輸出返回的結果
            alert('日記提交成功！'); // 提交成功的提示
            document.getElementById('diary-form').reset(); // 清空表單輸入
            window.location.href = "Homepage"; // 將頁面導向日記主頁面
        } else {
            alert('日記提交失敗！請重試。'); // 提交失敗的提示
        }
    } catch (error) {
        console.error('Error:', error); // 捕捉錯誤並輸出
    }
});
