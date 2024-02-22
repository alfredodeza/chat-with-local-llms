# Create a RAG with with FastAPI and a local LLM and Qdrant using your own data

In this lab you will implement the RAG pattern with your own data. Use the example code in this repository from the [RAG Notebook](./examples/2-rag/rag.ipynb) as reference as well as [API-based](./examples/3-api/chat.py) code. The end result should be in your own repository containing the complete code for the enhanced RAG pattern based on the example provided.

**Learning Objectives:**

* Implement the RAG pattern with your own data
* Apply your own data to solve a problem using RAG
* Understand how to leverage an LLM and a vector database like Qdrant for useful responses
* Use FastAPI connecting to a local LLM to provide fast local inferencing

## Steps

1. Create a new repository in your account for your project. Alternatively, you can use this repository as a starting point by forking the repository. [Use this link to create it in one step.](https://github.com/alfredodeza/chat-with-local-llms/generate).
2. Use the [RAG Notebook](./examples/2-rag/rag.ipynb) as reference as well as [API-based](./examples/3-api/chat.py)as a starting point
3. Port over the RAG from the notebook to the FastAPI instance
4. Run the LLM with Llamafile or Ollama to connect your application. Remember
   to add a `.env` file
5. Run the newly created API. You can use the following command (replace with
   your actual file): `uvicorn --host 0.0.0.0 solution:app --env-file .env`

Hint: You can take a look at the [solution file](./examples/3-api/solution.py)
if you are stuck. It has the fully working example that you can check to
validate your work.

## Concepts Covered

* Retrieval Augmented Generation
* Large Language Models using Llamafile
* Using Vector databases like Qdrant
* Creating embeddings with Sentence Transformers
* Using OpenAI's Python API to connect to the LLM and produce responses
* Using FastAPI with an LLM and using a `.env` file to load secrets for
  connections

By completing this lab you will have a working example of the RAG pattern with your own data using FastAPI. You will also have a better understanding of how to use local LLMs and vector databases to create useful responses for your applications.

**NOTE** For a vector database like Qdrant, it is recommended to have an actual
running instance _separately_ from your application. For demonstration
purposes, this repository uses an in-memory approach which is not suitable for
production environments.
