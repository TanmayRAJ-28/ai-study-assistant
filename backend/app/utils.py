import uuid

def generate_session_id():
    return str(uuid.uuid4())

def format_sources(source_documents):
    sources = []
    for doc in source_documents:
        page = doc.metadata.get('page', 'Unknown')
        excerpt = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        sources.append({"page": page, "excerpt": excerpt})
    return sources