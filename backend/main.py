
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.upload import router as upload_router
from routes.query import router as query_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(query_router)

@app.on_event("startup")
async def startup():
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs("vector_store/faiss_index", exist_ok=True)

# Add both routes
@app.get("/api/health")
@app.get("/health")
async def health():
    return {"status": "ok"}
