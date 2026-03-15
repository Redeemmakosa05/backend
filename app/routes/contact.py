from fastapi import APIRouter, HTTPException, Depends
from app.models import ContactMessage, ContactResponse
from app.database import get_db
from app.config import get_settings
from app.routes.auth import verify_token
import resend
import uuid
from datetime import datetime

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("", response_model=ContactResponse)
async def send_message(body: ContactMessage):
    s = get_settings()
    db = get_db()

    # Store in Supabase
    row = {
        "id": str(uuid.uuid4()),
        "name": body.name,
        "email": body.email,
        "subject": body.subject,
        "message": body.message,
        "created_at": datetime.utcnow().isoformat(),
    }
    result = db.table("contact_messages").insert(row).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to save message")

    # Send email via Resend
    try:
        resend.api_key = s.resend_api_key
        resend.Emails.send({
            "from": s.email_from,
            "to": s.email_to,
            "subject": f"Portfolio Contact: {body.subject}",
            "html": f"""
                <h2>New message from your portfolio</h2>
                <p><strong>Name:</strong> {body.name}</p>
                <p><strong>Email:</strong> {body.email}</p>
                <p><strong>Subject:</strong> {body.subject}</p>
                <hr/>
                <p>{body.message.replace(chr(10), '<br/>')}</p>
            """
        })
    except Exception as e:
        # Email failure shouldn't break the response — message is already saved
        print(f"Email send failed: {e}")

    return ContactResponse(id=row["id"], created_at=row["created_at"])


@router.get("", dependencies=[Depends(verify_token)])
def get_messages():
    """Admin only — get all contact messages."""
    db = get_db()
    result = db.table("contact_messages").select("*").order("created_at", desc=True).execute()
    return result.data
