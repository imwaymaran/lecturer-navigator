import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import re
from collections import defaultdict

import streamlit as st
from dotenv import load_dotenv

from backend.data_loader import load_pdfs_from_folder
from backend.splitter import split_documents
from backend.vectorstore import create_vectorstore
from backend.qa_chain import build_retrieval_qa

# Load environment
load_dotenv("env/.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    st.error("Missing OpenAI API key in .env file.")
    st.stop()

def run():
    st.title("Lecture Navigator")
    st.write("Ask questions based on your lecture slides.")

    if "qa" not in st.session_state:
        with st.spinner("Loading and processing lecture slides..."):
            raw_docs = load_pdfs_from_folder("data")
            chunks = split_documents(raw_docs)
            vectorstore = create_vectorstore(chunks)
            st.session_state.qa = build_retrieval_qa(vectorstore)

    query = st.text_input("Enter your question:")
    if query:
        with st.spinner("Searching for an answer..."):
            result = st.session_state.qa.invoke({"query": query})
            answer = result["result"].strip()

        st.subheader("Answer")
        st.write(answer)

        normalized = re.sub(r"[’‘]", "'", answer.lower())
        if not re.match(r"^i don'?t know[\.\!\s]*$", normalized):
            st.subheader("Sources cited in answer")
            source_map = defaultdict(set)

            for doc in result["source_documents"]:
                filename = os.path.basename(doc.metadata.get("source", ""))
                page = doc.metadata.get("page", "?")
                try:
                    page = int(page) + 1
                except:
                    pass
                source_map[filename].add(page)

            for file, pages in source_map.items():
                page_list = sorted(pages)
                page_str = ", ".join(str(p) for p in page_list)
                st.write(f"- {file} — slides {page_str}")
        else:
            st.info("The model couldn’t find an answer in the slides.")


if __name__ == "__main__":
    run()