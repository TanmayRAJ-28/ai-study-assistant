import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List

from app.embeddings import get_embeddings
from app.vector_store import (
    create_vector_store,
    save_vector_store,
    load_vector_store,
    merge_vector_stores
)
from app.rag_pipeline import process_pdf
from app.utils import generate_session_id

router = APIRouter()

UPLOAD_DIR = "data/uploads"


@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    session_id: str = Form(None)
):
    try:
        if not session_id:
            session_id = generate_session_id()

        embeddings = get_embeddings()
        combined_db = load_vector_store(embeddings, session_id)

        all_docs = []
        file_names = []

        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            docs = process_pdf(file_path)
            all_docs.extend(docs)
            file_names.append(file.filename)

        if not all_docs:
            raise HTTPException(status_code=400, detail="No valid documents")

        new_db = create_vector_store(all_docs, embeddings)

        if combined_db:
            combined_db = merge_vector_stores(combined_db, new_db)
        else:
            combined_db = new_db

        save_vector_store(combined_db, session_id)

        return {
            "session_id": session_id,
            "file_names": file_names,
            "chunk_count": len(all_docs),
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))