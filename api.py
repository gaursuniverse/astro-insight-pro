# api.py

from fastapi import FastAPI
from pydantic import BaseModel
from zodiac import get_zodiac_sign, get_time_insight
from model import llm
from translator import translator
import uvicorn
from datetime import datetime
from zoneinfo import ZoneInfo

app = FastAPI()

class Req(BaseModel):
    name: str = "Vishal Gaur"
    birth_date: str
    birth_time: str = "00:30"
    birth_place: str = "Hathras, Uttar Pradesh, India"
    language: str = "en"

@app.post("/predict")
def predict(req: Req):
    name = req.name.strip() or "Dear Vishal"
    zodiac = get_zodiac_sign(req.birth_date)
    current_ist_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%H:%M")
    time_insight = get_time_insight(current_ist_time)

    prompt = f"""
                You are a warm, poetic, spiritually intuitive astrologer who speaks with emotional depth. 
                Write a deeply uplifting, energizing, and beautifully crafted daily horoscope for {name}. 
                They are a {zodiac}, born at {req.birth_time} in {req.birth_place}.

                Use today's cosmic flow based on this time energy: {time_insight}.

                Your writing must:
                - Stay within 80 words
                - Feel personal, intimate, and encouraging
                - Blend cosmic symbolism with emotional reassurance
                - Give the reader a sense of strength, clarity, and renewed energy
                - Use gentle poetic language, but keep it understandable
                - Use simple, easy language suitable for Indian readers
                - End with a soft blessing or positive intention

                Do NOT mention that you are an AI, and do NOT break character.
                """

    insight_en = llm.generate_insight(prompt)
    insight = translator.translate(insight_en, req.language) if req.language != "en" else insight_en

    return {
        "zodiac": zodiac,
        "insight": insight,
        "language": req.language
    }

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, log_level="info")