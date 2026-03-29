from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== DATA =====
questions = [
    {
        "id": 1,
        "question": "React là thư viện của ngôn ngữ nào?",
        "options": ["Python", "JavaScript", "Java", "C#"],
        "correct_answer": "JavaScript"
    },
    {
        "id": 2,
        "question": "HTML là gì?",
        "options": ["Ngôn ngữ lập trình", "Ngôn ngữ đánh dấu", "Cơ sở dữ liệu", "Framework"],
        "correct_answer": "Ngôn ngữ đánh dấu"
    },
    {
        "id": 3,
        "question": "CSS dùng để làm gì?",
        "options": ["Xử lý logic", "Tạo database", "Thiết kế giao diện", "Viết API"],
        "correct_answer": "Thiết kế giao diện"
    },
    {
        "id": 4,
        "question": "Python thuộc loại ngôn ngữ nào?",
        "options": ["Compiled", "Interpreted", "Assembly", "Machine"],
        "correct_answer": "Interpreted"
    },
    {
        "id": 5,
        "question": "HTTP là viết tắt của gì?",
        "options": [
            "HyperText Transfer Protocol",
            "High Transfer Text Protocol",
            "Hyper Transfer Text Process",
            "Home Tool Transfer Protocol"
        ],
        "correct_answer": "HyperText Transfer Protocol"
    },
    {
        "id": 6,
        "question": "Framework dùng cho Python là?",
        "options": ["Django", "Laravel", "Spring", "React"],
        "correct_answer": "Django"
    },
    {
        "id": 7,
        "question": "Câu lệnh nào dùng để khai báo biến trong JavaScript?",
        "options": ["var", "int", "string", "define"],
        "correct_answer": "var"
    },
    {
        "id": 8,
        "question": "API là gì?",
        "options": [
            "Application Programming Interface",
            "Advanced Program Internet",
            "Application Process Input",
            "Auto Programming Interface"
        ],
        "correct_answer": "Application Programming Interface"
    }
]

# ===== MODEL =====
class Answer(BaseModel):
    question_id: int
    selected_answer: str

class SubmitRequest(BaseModel):
    answers: List[Answer]

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

# ===== API =====

# 🔹 Lấy câu hỏi
QUESTION_LIMIT = 7  # mặc định

@app.get("/questions")
def get_questions(limit: int = None):
    final_limit = limit if limit else QUESTION_LIMIT

    selected = random.sample(questions, min(final_limit, len(questions)))

    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in selected
    ]

# 🔹 Nộp bài
@app.post("/submit")
def submit_answers(data: SubmitRequest):
    score = 0
    results = []

    for ans in data.answers:
        q = next((q for q in questions if q["id"] == ans.question_id), None)

        if not q:
            continue

        is_correct = ans.selected_answer == q["correct_answer"] if ans.selected_answer else False

        if is_correct:
            score += 1

        results.append({
            "question_id": q["id"],
            "selected_answer": ans.selected_answer,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct
        })

    return {
        "total": len(results),
        "score": score,
        "details": results
    }

# 🔹 Thêm câu hỏi
@app.post("/add-question")
def add_question(q: QuestionCreate):
    if len(q.options) != 4:
        return {"error": "Phải có đúng 4 đáp án"}

    if q.correct_answer not in q.options:
        return {"error": "Đáp án đúng phải nằm trong options"}

    new_id = max([item["id"] for item in questions]) + 1 if questions else 1

    new_q = {
        "id": new_id,
        "question": q.question,
        "options": q.options,
        "correct_answer": q.correct_answer
    }

    questions.append(new_q)

    return {"message": "Thêm thành công", "data": new_q}

# 🔹 Xem tất cả câu hỏi
@app.get("/all-questions")
def get_all_questions():
    return questions
