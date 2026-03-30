from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

# ===== CONFIG =====
QUESTION_LIMIT = 5

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
        "description": "React dùng để xây dựng UI",
        "options": ["Python", "JavaScript", "Java", "C#"],
        "correct_answer": "JavaScript"
    },
    {
        "id": 2,
        "question": "HTML là gì?",
        "description": "Ngôn ngữ nền tảng web",
        "options": ["Ngôn ngữ lập trình", "Ngôn ngữ đánh dấu", "CSDL", "Framework"],
        "correct_answer": "Ngôn ngữ đánh dấu"
    },
    {
        "id": 3,
        "question": "CSS dùng để làm gì?",
        "description": "Thiết kế giao diện",
        "options": ["Logic", "DB", "UI", "API"],
        "correct_answer": "UI"
    },
    {
        "id": 4,
        "question": "Python là gì?",
        "description": "Ngôn ngữ phổ biến",
        "options": ["Compiled", "Interpreted", "ASM", "Machine"],
        "correct_answer": "Interpreted"
    },
    {
        "id": 5,
        "question": "HTTP là gì?",
        "description": "Giao thức web",
        "options": ["HTTP", "FTP", "SMTP", "TCP"],
        "correct_answer": "HTTP"
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
    description: str
    options: List[str]
    correct_answer: str

class QuestionUpdate(BaseModel):
    question: str | None = None
    description: str | None = None
    options: List[str] | None = None
    correct_answer: str | None = None
# ===== API =====

# 📋 GET QUESTIONS
@app.get("/questions")
def get_questions():
    selected = random.sample(questions, min(QUESTION_LIMIT, len(questions)))

    return [
        {
            "id": q["id"],
            "question": q["question"],
            "description": q["description"],
            "options": q["options"]
        }
        for q in selected
    ]


# 📝 SUBMIT
@app.post("/submit")
def submit_answers(data: SubmitRequest):
    score = 0
    results = []

    for ans in data.answers:
        q = next((q for q in questions if q["id"] == ans.question_id), None)
        if not q:
            continue

        is_correct = ans.selected_answer == q["correct_answer"]

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


# ➕ ADD QUESTION
@app.post("/add-question")
def add_question(q: QuestionCreate):
    if len(q.options) != 4:
        return {"error": "Phải có 4 đáp án"}

    if q.correct_answer not in q.options:
        return {"error": "Đáp án không hợp lệ"}

    new_id = max([item["id"] for item in questions]) + 1 if questions else 1

    new_q = {
        "id": new_id,
        "question": q.question,
        "description": q.description,
        "options": q.options,
        "correct_answer": q.correct_answer
    }

    questions.append(new_q)

    return {"message": "Thêm thành công", "data": new_q}


# ❌ DELETE QUESTION
@app.delete("/delete-question/{question_id}")
def delete_question(question_id: int):
    global questions

    q = next((q for q in questions if q["id"] == question_id), None)

    if not q:
        return {"message": "Không tìm thấy câu hỏi"}

    questions = [q for q in questions if q["id"] != question_id]

    return {"message": f"Đã xóa câu hỏi id = {question_id}"}


# ✏️ UPDATE QUESTION
@app.put("/update-question/{question_id}")
def update_question(question_id: int, updated_q: QuestionCreate):

    if len(updated_q.options) != 4:
        return {"error": "Phải có 4 đáp án"}

    if updated_q.correct_answer not in updated_q.options:
        return {"error": "Đáp án không hợp lệ"}

    for q in questions:
        if q["id"] == question_id:
            q["question"] = updated_q.question
            q["description"] = updated_q.description
            q["options"] = updated_q.options
            q["correct_answer"] = updated_q.correct_answer

            return {"message": "Cập nhật thành công", "data": q}

    return {"message": "Không tìm thấy câu hỏi"}

@app.patch("/update-question/{question_id}")
def update_question(question_id: int, updated_q: QuestionUpdate):

    for q in questions:
        if q["id"] == question_id:

            # chỉ cập nhật nếu có gửi lên
            if updated_q.question is not None:
                q["question"] = updated_q.question

            if updated_q.description is not None:
                q["description"] = updated_q.description

            if updated_q.options is not None:
                if len(updated_q.options) != 4:
                    return {"error": "Phải có 4 đáp án"}
                q["options"] = updated_q.options

            if updated_q.correct_answer is not None:
                # nếu đã có options mới thì check theo options mới
                opts = updated_q.options if updated_q.options else q["options"]

                if updated_q.correct_answer not in opts:
                    return {"error": "Đáp án không hợp lệ"}

                q["correct_answer"] = updated_q.correct_answer

            return {
                "message": "Cập nhật thành công",
                "data": q
            }

    return {"message": "Không tìm thấy câu hỏi"}

# 📌 XEM TẤT CẢ (để test CRUD)
@app.get("/all-questions")
def get_all():
    return questions
