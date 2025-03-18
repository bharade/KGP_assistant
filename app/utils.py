# import os
# import json
# import chromadb
# from chromadb.utils import embedding_functions
# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_ollama import ChatOllama


# # Initialize LLM
# local_llm = "deepseek-r1:1.5b"
# llm = ChatOllama(model=local_llm, temperature=0)
# llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")

# def initialize_vectorstore():
#     # Initialize ChromaDB client with persistence
#     client = chromadb.PersistentClient(path="vectorized_db")
#     if client.get_collection(name="iitkgp_data") is None:
#         print("Collection not found!")

#     # Create Embedding Function
#     sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

#     # Load the collection
#     collection = client.get_collection(name="iitkgp_data", embedding_function=sentence_transformer_ef)

#     # Create LangChain embeddings object (using HuggingFaceEmbeddings to match chromadb embeddings)
#     embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

#     # Create LangChain Chroma vectorstore
#     vectorstore = Chroma(client=client, collection_name="iitkgp_data", embedding_function=embeddings)

#     # Create retriever
#     retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
#     return vectorstore, retriever
    
# # Initialize retriever
# # def initialize_retriever(vectorstore):
# #     return vectorstore.as_retriever(k=8)

# # Format documents
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# # RAG prompt
# rag_prompt = """You are an assistant for question-answering tasks. 

# Here is the context to use to answer the question:

# {context} 

# Think carefully about the above context. 

# Now, review the user question:

# {question}

# Provide an answer to this questions using only the above context. 

# Use three sentences maximum and keep the answer concise.

# Answer:"""

import os
import json
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.vectorstores import Chroma #use the community vectorstore
from langchain_community.embeddings import HuggingFaceEmbeddings #use the community embedding
from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings as HFEmbeddings #use the huggingface embeddings.
from langchain_chroma import Chroma as LangChainChroma #use the chroma vectorstore

# Initialize LLM
local_llm = "deepseek-r1:1.5b"
llm = ChatOllama(model=local_llm, temperature=0)
llm_json_mode = ChatOllama(model=local_llm, temperature=0, format="json")

def initialize_vectorstore():
    # Initialize ChromaDB client with persistence
    client = chromadb.PersistentClient(path="vectorized_db")
    if client.get_collection(name="iitkgp_data") is None:
        print("Collection not found!")

    # Create Embedding Function
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-mpnet-base-v2")

    # Load the collection
    collection = client.get_collection(name="iitkgp_data", embedding_function=sentence_transformer_ef)

    # Create LangChain embeddings object (using HuggingFaceEmbeddings to match chromadb embeddings)
    embeddings = HFEmbeddings(model_name="all-mpnet-base-v2") #use the huggingface embeddings

    # Create LangChain Chroma vectorstore
    vectorstore = LangChainChroma(client=client, collection_name="iitkgp_data", embedding_function=embeddings) #use the chroma vectorstore

    # Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    return vectorstore, retriever

# Format documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG prompt
rag_prompt = """You are an assistant for question-answering tasks. 

Here is the context to use to answer the question:

{context} 

Think carefully about the above context. 

Now, review the user question:

{question}

Provide an answer to this questions using only the above context. 

Use three sentences maximum and keep the answer concise.

Answer:"""