# tools.py

import os
import requests
from dotenv import load_dotenv

# --- MODIFIED IMPORTS ---
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
# We are replacing the Google Embeddings with HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# --- TOOL 1: Weather Forecaster ---
def get_weather(city: str) -> str:
    """A tool that returns the current weather forecast for a given city."""
    print(f"--- Calling Weather Tool for city: {city} ---")
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key:
        return "Error: OpenWeatherMap API key not found."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        main_weather = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main_weather['temp']
        feels_like = main_weather['feels_like']
        return (f"Current weather in {city.title()}: "
                f"The temperature is {temp}°C (feels like {feels_like}°C) with {weather_desc}.")
    except Exception as e:
        return f"An error occurred while fetching weather data: {e}"

# --- TOOL 2 Functions: The Knowledge Base ---
def create_knowledge_base_retriever(persist_directory="./chroma_db"):
    """Creates and returns a retriever for the knowledge base."""
    print("--- Creating or loading knowledge base ---")
    
    # --- HERE IS THE MAIN CHANGE ---
    # We are now using a local, highly compatible embedding model.
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(persist_directory):
        print("Loading existing knowledge base.")
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_function
        )
        return vector_store.as_retriever()

    print("No existing knowledge base found. Creating a new one.")
    # Delete old incompatible database if it exists
    if os.path.exists(persist_directory):
        import shutil
        shutil.rmtree(persist_directory)

    loader = PyPDFDirectoryLoader("documents/")
    docs = loader.load()
    if not docs:
        raise ValueError("No documents found in 'documents' directory.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=persist_directory
    )
    print(f"--- Knowledge base created with {len(splits)} chunks. ---")
    return vector_store.as_retriever()

def get_agri_advice(query: str, retriever) -> str:
    """Provides agricultural advice by searching the expert documents using the provided retriever."""
    print(f"--- Calling Knowledge Base Tool for query: {query} ---")
    relevant_docs = retriever.get_relevant_documents(query)
    if not relevant_docs:
        return "I could not find any specific advice for your query in my documents."
    
    document_texts = [doc.page_content for doc in relevant_docs]
    return "\n\n---\n\n".join(document_texts)