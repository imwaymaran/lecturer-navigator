from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

custom_prompt = PromptTemplate.from_template("""
You are a helpful assistant answering questions based on lecture slides.

Only use the context below to answer the question.
If the answer is not in the context, say “I don’t know.”

Context:
{context}

Question: {question}
Answer:
""")

def build_retrieval_qa(db):
    retriever = db.as_retriever()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )
    return qa