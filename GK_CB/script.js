let questions = [];
let submitted = false;

async function loadQuestions() {
  submitted = false;

  const res = await fetch("http://127.0.0.1:8000/questions");
  questions = await res.json();

  const quizDiv = document.getElementById("quiz");
  quizDiv.innerHTML = "";

  document.getElementById("result").innerHTML = "";

  questions.forEach(q => {
    const div = document.createElement("div");

    let html = `<p>${q.question}</p>`;

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

  console.log(data); // debug

  submitted = true;

  // khóa chọn
  document.querySelectorAll("input[type=radio]").forEach(i => i.disabled = true);

  // khóa nút
  document.getElementById("submitBtn").disabled = true;

  const resultDiv = document.getElementById("result");

  let html = `<h3>Điểm: ${data.score}/${data.total}</h3>`;

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

  resultDiv.innerHTML = html;
}
