from fastapi import APIRouter, Depends
from app.database import get_db
from app.routes.auth import verify_token
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/{project_id}/view")
def increment_view(project_id: str):
    """Called by frontend on page load — increments view count."""
    db = get_db()

    # Upsert: create row if not exists, otherwise increment
    existing = db.table("project_views").select("*").eq("project_id", project_id).execute()

    if existing.data:
        current = existing.data[0]["views"]
        db.table("project_views").update({"views": current + 1}).eq("project_id", project_id).execute()
        return {"project_id": project_id, "views": current + 1}
    else:
        row = {"id": str(uuid.uuid4()), "project_id": project_id, "views": 1}
        db.table("project_views").insert(row).execute()
        return {"project_id": project_id, "views": 1}


@router.get("/{project_id}/view")
def get_views(project_id: str):
    db = get_db()
    result = db.table("project_views").select("views").eq("project_id", project_id).execute()
    views = result.data[0]["views"] if result.data else 0
    return {"project_id": project_id, "views": views}


@router.get("/views", dependencies=[Depends(verify_token)])
def all_views():
    """Admin — get view counts for all projects."""
    db = get_db()
    result = db.table("project_views").select("*").order("views", desc=True).execute()
    return result.data
