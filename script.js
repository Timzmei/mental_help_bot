let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#007BFF';

let usercard = document.getElementById("usercard");
let p = document.createElement("p");
try {
    let firstName = tg.initDataUnsafe.user.first_name;
    let lastName = tg.initDataUnsafe.user.last_name;
    p.innerText = `${lastName}${lastName}`;
} catch (error) {
    p.innerText = `Таинственный Незнакомец`;
}





usercard.appendChild(p);

let totalScore = 0;
let resultText = ``;
let questions_count = 0;
let fullTestName = '';
// let selectedValue = false;



const urlParams = new URLSearchParams(window.location.search);
const selectTest = urlParams.get('paramName');
console.log(selectTest);

// const selectTest = document.getElementById("selectTest");
const form = document.getElementById("quizForm");
const myHeading = document.getElementById("myHeading");

// Загрузить выбранный тест по умолчанию
// loadSelectedTest();

// selectTest.addEventListener("change", loadSelectedTest);



fetch(`${selectTest}.json`)
    .then(response => response.json())
    .then(data => {
        fullTestName = data.testName;
        myHeading.textContent = fullTestName;
        // Динамически создать форму с вопросами и ответами
        data.questions.forEach((q, index) => {
            // console.log(q);
            const questionDiv = document.createElement("div");
            questionDiv.classList.add("question");

            const questionP = document.createElement("p");
            questionP.className = "bold-red-text";
            questionP.textContent = (index + 1) + ". " + q.question;
            questions_count = index + 1;;

            questionDiv.appendChild(questionP);

            q.answers.forEach((ans, id) => {
                // console.log(ans);
                // console.log(ans.text);
                // console.log(ans.value);
                const answerInput = document.createElement("input");
                answerInput.type = "radio";
                answerInput.name = "q" + (index + 1);
                answerInput.value = ans.value.toString();

                const answerLabel = document.createElement("label");
                answerLabel.appendChild(answerInput);
                answerLabel.appendChild(document.createTextNode(" " + ans.text));

                questionDiv.appendChild(answerLabel);
            });

            form.insertBefore(questionDiv, document.getElementById("submit"));
        });
    })
    .catch(error => {
        console.error("Ошибка при загрузке теста: " + error);
    });

function getResultText(score, resultRanges) {
    for (const range of resultRanges) {
        if (score >= range.minScore && score <= range.maxScore) {
            return range.resultText;
        }
    }
    return "Результат не определен"; // Если результат не попадает ни в один интервал
}

document.getElementById("submit").addEventListener("click", function () {
    totalScore = 0;

    for (let i = 1; i <= questions_count; i++) {
        const selectedValue = document.querySelector(`input[name="q${i}"]:checked`);

        if (!selectedValue) {
            alert("Пожалуйста, ответьте на все вопросы.");
            return;
        } else {
            tg.MainButton.setText("Получить результат");
            tg.MainButton.show();
        }

        totalScore += parseInt(selectedValue.value);
    }

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = `Ваш результат: ${totalScore}`;
    // tg.sendData(`resultText`);

    fetch(`${selectTest}.json`)
        .then(response => response.json())
        .then(data => {
            // Получаем результат теста на основе баллов
            resultText = getResultText(totalScore, data.resultRanges);
            resultDiv.innerHTML += `<br>${resultText}`;
            // Выводим результат на странице или делаем с ним что-то еще
            // console.log(resultText);
    });
    
});



Telegram.WebApp.onEvent("mainButtonClicked", function(){
    selectedAnswers = [];

    for (let i = 1; i <= questions_count; i++) {
        const selectedValue = document.querySelector(`input[name="q${i}"]:checked`);

        if (!selectedValue) {
            selectedAnswers.push({ question: `Вопрос ${i}`, answer: 'Ответ не выбран' });
        } else {
            const questionText = document.querySelector(`.question:nth-child(${i}) p`).textContent;
            const answerText = selectedValue.parentElement.textContent.trim();
            selectedAnswers.push({ question: questionText, answer: answerText });
        }
    }
    console.log(resultText);
    selectedAnswers.push({ test_name: fullTestName, result: totalScore, text_result: resultText });
    tg.sendData(selectedAnswers);
    Telegram.WebApp.close();

});

