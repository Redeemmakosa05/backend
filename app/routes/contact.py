# app/routes/contact.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
import resend
import os

router = APIRouter()


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


@router.post("/contact")
async def send_contact(form: ContactForm):
    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="RESEND_API_KEY not set on server"
        )

    resend.api_key = api_key  # set per-request so it picks up env var at runtime

    email_from = os.getenv("EMAIL_FROM")
    email_to = os.getenv("EMAIL_TO")

    if not email_from or not email_to:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="EMAIL_FROM or EMAIL_TO not configured on server"
        )

    try:
        resp = resend.Emails.send({
            "from": email_from,
            "to": email_to,
            "subject": f"{form.subject} — from {form.name}",
            "reply_to": form.email,
            "html": (
                f"<h3>New Portfolio Message</h3>"
                f"<p><b>Name:</b> {form.name}</p>"
                f"<p><b>Email:</b> {form.email}</p>"
                f"<p><b>Subject:</b> {form.subject}</p>"
                f"<p><b>Message:</b></p>"
                f"<p>{form.message}</p>"
            ),
        })
        return {"status": "sent", "id": resp.get("id") if isinstance(resp, dict) else str(resp)}
    except Exception as e:
        print("EMAIL ERROR:", repr(e))  # appears in Railway logs
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Email provider error: {repr(e)}"
        )
