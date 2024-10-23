import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from consts import llm_model_name

# Load .env variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_stream = ChatOpenAI(max_retries=5, temperature=0,
                        model_name=llm_model_name, streaming=True, callbacks=[StreamingStdOutCallbackHandler()])  # type: ignore

llm_non_stream = ChatOpenAI(
    temperature=0, model_name=llm_model_name, max_retries=5,)  # type: ignore

# llm_stream = ChatOllama(model="llama3.2:latest", base_url="")

# llm_non_stream = ChatOllama(model="llama3.2:latest", base_url="")