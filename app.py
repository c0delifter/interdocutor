from dotenv import load_dotenv
from dotenv import find_dotenv
import streamlit as streamlit
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

import os

def main():
    load_dotenv(find_dotenv())
    os.getenv("OPEN_API_KEY")
    initiate_streamlit()

def initiate_streamlit():
    streamlit.set_page_config(page_title="interdocutor.ai")
    streamlit.title("interDOCutor 🤖")
    streamlit.subheader("Interact with your PDF documents ChatGPT style")

    pdf = streamlit.file_uploader("Upload file below", type=["pdf"])
    create_upload_file_widget(pdf)

def create_upload_file_widget(pdf):
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text+=page.extract_text()

        chunks = create_chunks(text)
        knowledge_base = create_knowledge_base(chunks)
        create_qna_widget(knowledge_base)

def create_qna_widget(knowledge_base):
    question = streamlit.text_input("Ask a question about your PDF")
    create_response_widget(question, knowledge_base)    

def create_response_widget(question: str, knowledge_base):
    if question:
        knowledge_base_filtered = knowledge_base.similarity_search(question)
        response = generate_response(question, knowledge_base_filtered)
        streamlit.write(response)

def generate_response(question: str, knowledge_base_filtered: list[str]):
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    response = chain.run(input_documents=knowledge_base_filtered, question=question)
    return response

def create_chunks(text: str):
    text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

    chunks = text_splitter.split_text(text)
    return chunks

def create_knowledge_base(chunks: list[str]):
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    return knowledge_base

if __name__ == "__main__":
    main()