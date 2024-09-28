function getData() {
    const savedData = JSON.parse(sessionStorage.getItem('question_and_answer'));
    if (savedData) {
        document.getElementById('diaryEntry').value = 
            "Question: " + savedData.question + "\nAnswer: " + savedData.answer;
    }
};