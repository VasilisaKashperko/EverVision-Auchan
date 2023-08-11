from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.storage import LocalFileStore
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
import openai
import streamlit as st


LANGCHAIN_CONFIG = {
    'cache': './cache/',
    'documents': './docs/auchan.csv',
    'top_k': 5,
    'fetch_k': 50
}


def langchain_load_db():
    # use the same key as in main
    openai.api_key = st.secrets['OPENAI_API_KEY']

    # default OpenAI embedding for documents
    underlying_embeddings = OpenAIEmbeddings()

    # local filestore
    fs = LocalFileStore(LANGCHAIN_CONFIG['cache'])

    # create cached embeddings, it will be much faster at second use
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings,
        fs,
        namespace=underlying_embeddings.model
    )

    # split raw csv file into langchain documents
    loader = CSVLoader(file_path=LANGCHAIN_CONFIG['documents'])
    documents = loader.load()

    # make vector db
    db = FAISS.from_documents(documents, cached_embedder)

    return db


def langchain_find_docs(db, question):
    # find similar documents
    docs = db.similarity_search_with_relevance_scores(
        question,
        k=LANGCHAIN_CONFIG['top_k'],
        fetch_k=LANGCHAIN_CONFIG['fetch_k']
    )

    # sort by score
    docs = sorted(docs, key=lambda x: x[1], reverse=True)
    return docs


def langchain_parse_docs(docs):
    parsed = ''
    for doc in docs:
        parsed += doc[0].page_content.replace('\n', '. ') + '.\n'
    return parsed


if __name__ == '__main__':
    db = langchain_load_db()
    q = 'Сколько стоит курица?'
    docs = langchain_find_docs(db, q)
    context = langchain_parse_docs(docs)
    print(context)
