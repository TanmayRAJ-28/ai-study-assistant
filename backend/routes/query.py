
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.embeddings import get_embeddings
from app.vector_store import load_vector_store
from app.llm import get_llm
from app.rag_pipeline import get_qa_chain
from app.utils import format_sources

router = APIRouter()


def format_chat_history(chat_history):
    """Convert frontend format → LangChain format"""
    formatted = []

    for i in range(0, len(chat_history), 2):
        if i + 1 < len(chat_history):
            user = chat_history[i]["content"]
            assistant = chat_history[i + 1]["content"]
            formatted.append((user, assistant))

    return formatted


@router.post("/query")
async def query_rag(payload: dict):
    try:
        session_id = payload.get("session_id")
        question = payload.get("question")
        file_name = payload.get("file_name")
        chat_history = payload.get("chat_history", [])

        if not session_id or not question:
            raise HTTPException(status_code=400, detail="Missing fields")

        embeddings = get_embeddings()
        db = load_vector_store(embeddings, session_id)

        if not db:
            raise HTTPException(status_code=404, detail="Session not found")

        llm = get_llm()
        # Optionally restrict retrieval to a single uploaded file
        chain = get_qa_chain(db, llm, file_name=file_name)

        formatted_history = format_chat_history(chat_history)

        async def event_stream():
            result = chain.invoke({
                "question": question,                # ✅ FIXED
                "chat_history": formatted_history # ✅ FIXED
            })

            answer = result.get("answer", "")
            sources = format_sources(result.get("context", []))  # ✅ FIXED

            # stream tokens
            for word in answer.split():
                yield f"data: {json.dumps({'token': word})}\n\n"

            # send sources at end
            yield f"data: {json.dumps({'sources': sources})}\n\n"

        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))