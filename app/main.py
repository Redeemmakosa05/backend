from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import auth, contact, projects, blog

s = get_settings()

app = FastAPI(
    title="Redemption Makosa — Portfolio API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[s.frontend_url, "http://localhost:3000", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(projects.router)
app.include_router(blog.router)


@app.get("/")
def health():
    return {"status": "ok", "api": "Redemption Makosa Portfolio API v1.0"}
    
from pydantic import BaseModel
import resend
import os

resend.api_key = os.getenv("RESEND_API_KEY")

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/contact")
async def send_contact(form: ContactForm):

    resend.Emails.send({
        "from": os.getenv("EMAIL_FROM"),
        "to": os.getenv("EMAIL_TO"),
        "subject": f"Portfolio Message from {form.name}",
        "html": f"""
        <p><b>Name:</b> {form.name}</p>
        <p><b>Email:</b> {form.email}</p>
        <p><b>Message:</b></p>
        <p>{form.message}</p>
        """
    })

    return {"status": "sent"}
