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

# 🔹 Lấy câu hỏi (random 5 câu nếu có nhiều)
@app.get("/questions")
def get_questions():
    selected_questions = random.sample(questions, min(5, len(questions)))

    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        for q in selected_questions
    ]


# 🔹 Nộp bài
@app.post("/submit")
def submit_answers(data: SubmitRequest):
    score = 0
    results = []

    # check số lượng câu
    if len(data.answers) > len(questions):
        return {"error": "Số câu trả lời không hợp lệ"}

    for ans in data.answers:
        # tìm câu hỏi
        q = None
        for question in questions:
            if question["id"] == ans.question_id:
                q = question
                break

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
    new_id = max([item["id"] for item in questions]) + 1 if questions else 1

    new_question = {
        "id": new_id,
        "question": q.question,
        "options": q.options,
        "correct_answer": q.correct_answer
    }

    questions.append(new_question)

    return {
        "message": "Thêm câu hỏi thành công",
        "data": new_question
    }


# 🔹 Xem tất cả câu hỏi (có đáp án)
@app.get("/all-questions")
def get_all_questions():
    return questions


# 🔹 Xóa câu hỏi
@app.delete("/delete-question/{question_id}")
def delete_question(question_id: int):
    global questions

    questions = [q for q in questions if q["id"] != question_id]

    return {"message": "Đã xóa câu hỏi"}