// 決定顯示幾個
function Button_show() {

    fetch('/get-talk-num') 
        .then(response => response.json())  // 解析 JSON 響應
        .then(data => {
            console.log(data.response);  // 顯示返回的數字
            var talk_num = parseInt(data.response, 10);

            if (talk_num > 0) {
                const element = document.getElementById("button_1");
                element.style.display = "block"
            }
            if (talk_num > 1) {
                const element = document.getElementById("button_2");
                element.style.display = "block"
            }
            if (talk_num > 2) {
                const element = document.getElementById("button_3");
                element.style.display = "block"
            }
            
        })
        .catch(error => console.error('錯誤:', error));  // 捕獲並顯示錯誤
}

// 將頁面導向日記主頁面
function AddDreamWeaver(num_table) { window.location.href = `DreamWeaver?num_table=${num_table}`; }

// 點擊標題 -> 回到主頁
function BackHome() { window.location.href = "Homepage"; }

Button_show()