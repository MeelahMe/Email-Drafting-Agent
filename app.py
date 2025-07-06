from fastapi import FastAPI
from pydantic import BaseModel
from entrypoint import compose_email  # ← import from root entrypoint.py


class EmailRequest(BaseModel):
    bullets: str
    sender_name: str = "Your Name"
    tone: str = "formal"
    language: str = "en"


app = FastAPI()


@app.post("/draft_email")
async def draft_email(req: EmailRequest):
    result = compose_email(
        bullets=req.bullets,
        sender_name=req.sender_name,
        tone=req.tone,
        language=req.language,
    )
    return {"subject": result["subject"], "email": result["email"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
