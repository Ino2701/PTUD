let questions = [];
let submitted = false;

let time = 0;
let timerInterval;

function startTimer() {
  time = 0;

  timerInterval = setInterval(() => {
    time++;
    document.getElementById("timer").innerText = "Thời gian: " + time + "s";
  }, 1000);
}

async function loadQuestions() {
  submitted = false;

  startTimer();

  const res = await fetch("http://127.0.0.1:8000/questions");
  questions = await res.json();

  const quizDiv = document.getElementById("quiz");
  quizDiv.innerHTML = "";

  document.getElementById("result").innerHTML = "";

  questions.forEach(q => {
    const div = document.createElement("div");

    let html = `
      <p><b>${q.question}</b></p>
      <p style="color: gray;">${q.description}</p>
    `;

    q.options.forEach(opt => {
      html += `
        <label>
          <input type="radio" name="q${q.id}" value="${opt}">
          ${opt}
        </label><br>
      `;
    });

    div.innerHTML = html;
    quizDiv.appendChild(div);
    document.getElementById("restartBtn").style.display = "none";
  });

  document.getElementById("submitBtn").disabled = false;
}

async function submitQuiz() {
  const answers = questions.map(q => {
    const selected = document.querySelector(`input[name="q${q.id}"]:checked`);
    return {
      question_id: q.id,
      selected_answer: selected ? selected.value : ""
    };
  });

  const res = await fetch("http://127.0.0.1:8000/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ answers })
  });

  const data = await res.json();

  clearInterval(timerInterval);

  submitted = true;

  document.querySelectorAll("input[type=radio]").forEach(i => i.disabled = true);
  document.getElementById("submitBtn").disabled = true;

  const resultDiv = document.getElementById("result");

  let html = `<h3>Điểm: ${data.score}/${data.total}</h3>`;
  html += `<p>Thời gian làm bài: ${time} giây</p>`;

  data.details.forEach(d => {
    html += `
      <p>
        Câu ${d.question_id}: 
        Bạn chọn: ${d.selected_answer || "Không chọn"} 
        → ${d.is_correct ? "Đúng" : "Sai"} 
        (Đáp án: ${d.correct_answer})
      </p>
    `;
  });
document.getElementById("restartBtn").style.display = "inline-block";
  resultDiv.innerHTML = html;
}
function goToAdmin() {
  window.location.href = "admin.html";
}
function restartQuiz() {
  clearInterval(timerInterval);

  time = 0;
  submitted = false;
  questions = [];

  document.getElementById("timer").innerText = "Thời gian: 0s";
  document.getElementById("quiz").innerHTML = "";
  document.getElementById("result").innerHTML = "";

  document.getElementById("submitBtn").disabled = false;
  document.getElementById("restartBtn").style.display = "none";
}
