from pathlib import Path
import pickle

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.retrievers import TFIDFRetriever

def init_gpt(file_name):
    prompt = ChatPromptTemplate.from_template("""あなたはカスタマーサービスです。日本語で答えてください。：
    <context>
    {context}
    </context>
    Question: {input}""")
    llm = ChatOpenAI(model='gpt-4-0125-preview')
    document_chain = create_stuff_documents_chain(llm, prompt)
    vector = FAISS.load_local(f'./models/vector/{file_name}.pkl', OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain

def create_vector(file_name):
    path_str = f'./models/vector/{file_name}.pkl'
    if not Path(path_str).exists():
        loader = PyPDFLoader(f"./assets/{file_name}")
        pages = loader.load_and_split()
        vector = FAISS.from_documents(pages, OpenAIEmbeddings())
        vector.save_local(Path(path_str))


def search(prompt, retrieval_chain):
    response = retrieval_chain.invoke({"input": prompt})
    return response['answer']
