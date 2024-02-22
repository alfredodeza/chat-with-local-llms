from fastapi import FastAPI, Response
from pydantic import BaseModel
import pandas as pd
import os
from os.path import dirname
import openai
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer


openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME")


app = FastAPI()
current_directory = dirname(os.path.realpath(__file__))
root = dirname(dirname(current_directory))
csv_file = os.path.join(root, 'top_rated_wines.csv')
df = pd.read_csv(csv_file)
df = df[df['variety'].notna()]
data = df.sample(700).to_dict('records') # Get only 700 records. More records will make it slower to index


# Load the encoder
encoder = SentenceTransformer('all-MiniLM-L6-v2')


# Not for production environments! Don't use in memory databases unless it is for testing and demoing
qdrant = QdrantClient(":memory:")

# Create collection to store wines
qdrant.recreate_collection(
    collection_name="top_wines",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
        distance=models.Distance.COSINE
    )
)

# vectorize!
# Note that for Coursera we use an older way of Qdrant doing the uploads using Records instead of Points
qdrant.upload_records(
    collection_name="top_wines",
    records=[
        models.Record(
            id=idx,
            vector=encoder.encode(doc["notes"]).tolist(),
            payload=doc
        ) for idx, doc in enumerate(data) # data is the variable holding all the wines
    ]
)

class Body(BaseModel):
    text: str


def ai_chat(user_message, extra_context=""):
    message_text = [
       {"role":"system","content":"You are a wine specialist. Your top priority is to help guide users find the best wine.You always come with good suggestions"},
       {"role": "user", "content": user_message},
       {"role": "assistant", "content": extra_context}
    ]
    completion = openai.ChatCompletion.create(
      model=model_name,
      messages=message_text,
      temperature=0.5,
      max_tokens=400,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    return completion


@app.post('/generate')
def generate(body: Body):
    # Search time for awesome wines!
    hits = qdrant.search(
        collection_name="top_wines",
        query_vector=encoder.encode(body.text).tolist(),
        limit=3
    )
    # Debug the output from the Vector Database
    print(hits)
    # define a variable to hold the search results
    search_results = [hit.payload for hit in hits]
    completion = ai_chat(body.text, str(search_results))
    return {"text": completion['choices'][0]['message']['content']}
