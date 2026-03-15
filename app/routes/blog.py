from fastapi import APIRouter, HTTPException, Depends
from app.models import PostCreate, PostUpdate, Post
from app.database import get_db
from app.routes.auth import verify_token
import uuid
from datetime import datetime

router = APIRouter(prefix="/blog", tags=["blog"])


@router.get("")
def get_posts(published_only: bool = True):
    db = get_db()
    query = db.table("posts").select("*").order("created_at", desc=True)
    if published_only:
        query = query.eq("published", True)
    result = query.execute()
    return result.data


@router.get("/{slug}")
def get_post(slug: str):
    db = get_db()
    result = db.table("posts").select("*").eq("slug", slug).eq("published", True).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Post not found")
    return result.data[0]


@router.post("", dependencies=[Depends(verify_token)])
def create_post(body: PostCreate):
    db = get_db()

    # Check slug uniqueness
    existing = db.table("posts").select("id").eq("slug", body.slug).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Slug already exists")

    now = datetime.utcnow().isoformat()
    row = {
        "id": str(uuid.uuid4()),
        "title": body.title,
        "slug": body.slug,
        "excerpt": body.excerpt,
        "content": body.content,
        "published": body.published,
        "tags": body.tags,
        "created_at": now,
        "updated_at": now,
    }
    result = db.table("posts").insert(row).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create post")
    return result.data[0]


@router.put("/{post_id}", dependencies=[Depends(verify_token)])
def update_post(post_id: str, body: PostUpdate):
    db = get_db()
    updates = body.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updates["updated_at"] = datetime.utcnow().isoformat()
    result = db.table("posts").update(updates).eq("id", post_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Post not found")
    return result.data[0]


@router.delete("/{post_id}", dependencies=[Depends(verify_token)])
def delete_post(post_id: str):
    db = get_db()
    db.table("posts").delete().eq("id", post_id).execute()
    return {"deleted": post_id}
