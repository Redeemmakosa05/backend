# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import auth, contact, projects, blog

s = get_settings()

app = FastAPI(
    title="Redemption Makosa Portfolio API",
    version="1.0.0",
)

# CORS must be added BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://portfolio-frontend-gules-nine.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ],
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
