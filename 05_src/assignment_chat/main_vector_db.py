import os
from dotenv import load_dotenv

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings


load_dotenv('../.secrets')
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Missing OPENAI_API_KEY environment variable")


#######################################
# Load the docs
#######################################
loader = CSVLoader(
    file_path="data/mental.csv",
    metadata_columns=["Exercise Name"]
)

data = loader.load()
print(data[1].model_dump())


#######################################
# Initialize the embedding model
#######################################
embeddings_model = OpenAIEmbeddings(
    openai_api_base="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    openai_api_key="any value", # The Gateway expects this literal string
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')},
    model="text-embedding-3-small"
)

#######################################
# Create the Vector Store with Persistence
#######################################
persist_directory = "./chroma_db"

vector_db = Chroma.from_documents(
    documents=data,
    embedding=embeddings_model,
    persist_directory=persist_directory
)

print(f"Database saved to {persist_directory}")


