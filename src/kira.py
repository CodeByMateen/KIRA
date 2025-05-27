from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
import requests
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
vector_id = os.getenv("VECTOR_STORE_ID")

client = OpenAI(api_key=api_key)


def create_file(client, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(file=file_tuple, purpose="assistants")
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(file=file_content, purpose="assistants")
    print(result.id)
    return result.id


def add_s3_file_to_vector_store(s3_url):
    file_id = create_file(client, s3_url)
    vector_store = client.vector_stores.create(name="knowledge_base")
    results = client.vector_stores.files.create(
        vector_store_id=vector_store.id, file_id=file_id
    )
    print(f"Vector Store ID: {vector_store.id}")
    print(f"File added results: {results}")
    return vector_store.id


def vector_store_id(file_path):
    # Replace with your own file path or URL
    file_id = create_file(client, file_path)
    vector_store = client.vector_stores.create(name="knowledge_base")
    print(vector_store.id)
    results = client.vector_stores.files.create(
        vector_store_id=vector_store.id, file_id=file_id
    )
    print(results)
    return vector_store.id


def chat_with_gpt(query):
    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=query,
            tools=[{"type": "file_search", "vector_store_ids": [vector_id]}],
        )
        return response.output_text
    except Exception as e:
        return f"An error occurred: {e}"


# if __name__ == "__main__":
#     user_query = ""
#     answer = chat_with_gpt(user_query)
#     print("Answer:", answer)
