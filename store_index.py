from src.helper import load_documents,split_docs,download_hugginface_hub_embeddings
import os
from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore")

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore


os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]="MBSD-chatbot"
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)

docs = load_documents("data/MBSD Book.pdf")

text_chunks = split_docs(docs)

index_name = "mbsd-chatbot"

embeddings = download_hugginface_hub_embeddings()

##Initiliaze the pine cone vector store
vectorstore_from_docs = PineconeVectorStore.from_documents(
text_chunks,
index_name=index_name,
embedding=embeddings
)

#Initialize the retriever
retriever = vectorstore_from_docs.as_retriever()

system_prompt = (
"You are an expert assistant responsible for answering questions based on my MBSD book. "
"Your role is similar to that of a highly knowledgeable teacher who provides well-analyzed, professional responses. "
"Use the retrieved context to answer the question accurately and concisely. "
"If the answer is not clear from the context, explicitly state that the information is not available. "
"Deliver responses in a formal, professional tone, and aim for clarity in no more than three sentences. "
"If relevant, break down the explanation into bullet points for ease of understanding."
"\n\n"
"{context}"
)


prompt = ChatPromptTemplate.from_messages(
[
("system", system_prompt),
("human", "{input}"),
]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

while True:
    user_input = input("Student: ")  # Get user input
    if user_input == "hi":
        print("Hi, I am an MBSD book assistant. How can I help you?")
    elif user_input == "bye":
        print("Bye! Hope you learned something from me.")
        break
    else:
        response = chain.invoke({"MBSD Assistant": user_input})  # Pass user input correctly
        print(response["answer"])  # Print the final answer



