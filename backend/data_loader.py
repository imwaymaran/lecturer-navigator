import os
from langchain_community.document_loaders import PyPDFLoader

def load_pdfs_from_folder(folder_path):
    lecture_slides = []
    for file in os.listdir(folder_path):
        if file.endswith('.pdf'):
            file_path = os.path.join(folder_path, file)
            loader = PyPDFLoader(file_path)
            docs = loader.load()

            # Inject metadata into page_content
            for doc in docs:
                filename = os.path.basename(doc.metadata.get("source", ""))
                page = doc.metadata.get("page", "?")
                try:
                    page = int(page) + 1
                except:
                    pass
                header = f"[{filename} — slide {page}]"
                doc.page_content = f"{header}\n\n{doc.page_content}"

            lecture_slides.extend(docs)
    return lecture_slides