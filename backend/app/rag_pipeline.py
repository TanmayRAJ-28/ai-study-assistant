from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import ConversationalRetrievalChain


def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(docs)


def get_qa_chain(db, llm, file_name=None):
    """Build QA chain.

    If ``file_name`` is provided, restrict retrieval to chunks coming from
    that uploaded file only, using the ``source`` metadata stored by
    ``PyPDFLoader``.
    """

    search_kwargs = {"k": 3}

    # ``source`` is the original file path, e.g. "data/uploads/<file_name>"
    if file_name:
        search_kwargs["filter"] = {"source": f"data/uploads/{file_name}"}

    retriever = db.as_retriever(search_kwargs=search_kwargs)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        verbose=False
    )
