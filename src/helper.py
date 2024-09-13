from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


#Load the documents
def load_documents(data):
  loader = PyPDFLoader(data)
  documents = loader.load()
  return documents

#Split the documents into the chunks
def split_docs(extracted_data):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500,chunk_overlap=20)
  text_chunks = text_splitter.split_documents(extracted_data)
  return text_chunks

#Embedding model
def download_hugginface_hub_embeddings():
  embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
  return embeddings

