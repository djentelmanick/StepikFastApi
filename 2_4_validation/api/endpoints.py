from api.db import db_feedbacks
from api.schemas import Feedback
from fastapi import APIRouter


feedback = APIRouter(prefix="/feedback")


@feedback.get("")
async def get_feedbacks():
    return db_feedbacks


@feedback.post("")
async def add_feedback(new_feedback: Feedback, is_premium: bool = False):
    db_feedbacks.append(new_feedback.model_dump())
    answer = f"Спасибо, {new_feedback.name}! Ваш отзыв сохранён."
    if is_premium:
        answer += " Он будет рассмотрен в приоритетном порядке!"
    return {"message": answer}
