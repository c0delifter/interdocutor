# Introducing interDOCutor 🤖
A simple but nifty web app to interact with your PDF documents ChatGPT style. 

Technologies used:

- Python
- Streamlit
- Docker (with Docker Compose)
- LangChain
- OpenAI Embeddings

# How to Run

Step #1: Update the .env file with your own OpenAI API key. Instructions on how to obtain said key [can be found here](https://platform.openai.com/docs/quickstart?context=python)

Step #2: Spin up a new Docker container by opening a terminal and typing the following command

```
> docker compose up
```

# Known limitations

What you're seeing a version 1.0.0 of the product. It uses OpenAI's embeddings model to generate the vector embeddings (which costs $).

Additionally, there's no persistent storage to hold the knowledge base. Future version(s) of the app will have a Vector Database (Chroma, Pinecone, Milvus, etc.) attached.

Last but not least: Running the embeddings model on your own CPU is not scalable long-term. In the future, both the LLM and the embeddings model will be hosted externally.