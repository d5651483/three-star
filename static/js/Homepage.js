let currentIndex = 0;
        const slides = document.querySelector('.slides');
        const slideItems = document.querySelectorAll('.slide');
        const totalSlides = slideItems.length; // 原本的幻燈片數量
        const dots = document.querySelectorAll('.dot'); // 取得所有點
        let intervalId;

        // 克隆第一張幻燈片，並追加到幻燈片末尾
        const firstSlideClone = slideItems[0].cloneNode(true);
        slides.appendChild(firstSlideClone); // 將克隆的幻燈片添加到末尾

        function showSlide(index) {
            const offset = index * -100;
            slides.style.transform = `translateX(${offset}%)`;
            slides.style.transition = 'transform 0.5s ease'; // 保持過渡效果
            updateDots(index >= totalSlides ? 0 : index); // 更新點，克隆時顯示第一個點
        }

        function updateDots(index) {
            dots.forEach((dot, i) => {
                dot.classList.remove('active'); // 移除所有點的 active 樣式
                if (i === index) {
                    dot.classList.add('active'); // 為當前幻燈片對應的點添加 active 樣式
                }
            });
        }

        // 監聽過渡結束事件，當到達克隆的第一張時無縫跳回真正的第一張
        slides.addEventListener('transitionend', () => {
            if (currentIndex === totalSlides) {
                slides.style.transition = 'none'; // 禁用過渡效果
                slides.style.transform = 'translateX(0%)'; // 無縫跳回真正的第一張
                currentIndex = 0; // 重置索引
                setTimeout(() => {
                    slides.style.transition = 'transform 0.5s ease'; // 恢復過渡效果
                }, 50); // 短暫延遲後恢復過渡效果
            }
        });

        // 設置自動播放功能
        function startSlideShow() {
            intervalId = setInterval(() => {
                currentIndex++;

                if (currentIndex > totalSlides) {
                    currentIndex = totalSlides; // 顯示克隆的第一張幻燈片
                }
                showSlide(currentIndex);
            }, 4000); // 保持每 4 秒切換一次
        }

        // 停止自動播放
        function stopSlideShow() {
            clearInterval(intervalId);
        }

        // 重新啟動自動播放
        function restartSlideShow() {
            stopSlideShow(); // 停止當前播放
            startSlideShow(); // 重新啟動自動播放
        }

        // 左箭頭按鈕功能：顯示上一張幻燈片
        function prevSlide() {
            stopSlideShow(); // 停止自動播放
            currentIndex--;

            if (currentIndex < 0) {
                currentIndex = totalSlides - 1; // 回到克隆的第一張
                slides.style.transition = 'none'; // 禁用過渡效果
                slides.style.transform = `translateX(${-currentIndex * 100}%)`; // 立即移動到克隆的第一張
                setTimeout(() => {
                    slides.style.transition = 'transform 0.5s ease'; // 恢復過渡效果
                }, 50); // 延遲恢復過渡效果
            } else {
                showSlide(currentIndex); // 顯示上一張
            }

            // 更新點
            updateDots(currentIndex >= totalSlides ? 0 : currentIndex);
            restartSlideShow(); // 重啟自動播放
        }

        // 右箭頭按鈕功能：顯示下一張幻燈片
        function nextSlide() {
            stopSlideShow(); // 停止自動播放
            currentIndex++;

            if (currentIndex > totalSlides) {
                currentIndex = totalSlides; // 克隆的第一張
            }

            showSlide(currentIndex); // 顯示下一張
            // 更新點
            updateDots(currentIndex >= totalSlides ? 0 : currentIndex);
            restartSlideShow(); // 重啟自動播放
        }

        // 點擊點跳轉到對應幻燈片
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                stopSlideShow(); // 點擊點時停止自動播放
                currentIndex = index; // 更新當前索引
                showSlide(currentIndex); // 顯示對應幻燈片
                restartSlideShow(); // 重啟自動播放
            });
        });

        // 初始化時更新點的狀態
        updateDots(currentIndex); // 確保第一個點為 active

        // 啟動幻燈片自動播放
        startSlideShow();



function DairyAnswer() {    
    window.location.href = "DairyHome"; // 將頁面導向日記主頁面
}
function DreamweaverAnswer() {    
    window.location.href = "DreamWeaverHome"; // 將頁面導向織夢機主頁面
}
function popupAnswer() {    
    window.location.href = "QuestionShow"; // 將頁面導向織夢機主頁面
}
function signin() {    
    window.location.href = "signin"; // 將頁面導向織夢機主頁面
}
function signup() {    
    window.location.href = "signup"; // 將頁面導向織夢機主頁面
}
// 點擊標題 -> 回到主頁
function BackHome() {window.location.href = "Homepage";}