from fastapi import FastAPI
from pydantic import BaseModel
from entrypoint import compose_email  
from fastapi.responses import JSONResponse


app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def health_check():
    """
    Simple health check so GET / returns 200 instead of 404.
    """
    return {"status": "Email Drafting Agent is up – POST to /draft_email"}

@app.get("/favicon.ico")
async def favicon():
    """
    Suppress favicon requests with a 204 No Content.
    """
    return JSONResponse(status_code=204, content=None)


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
