from backend.data_loader import load_pdfs_from_folder
from backend.splitter import split_documents
from backend.vectorstore import create_vectorstore
from backend.qa_chain import build_retrieval_qa

def initialize_qa(data_folder="data"):
    raw_docs = load_pdfs_from_folder(data_folder)
    chunks = split_documents(raw_docs)
    vectorstore = create_vectorstore(chunks)
    qa = build_retrieval_qa(vectorstore)
    return qa