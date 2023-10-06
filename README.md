# ademe_rag

## Description
Allow to build a Rag based on the ADEME baseCarbone.

Has been tested using the version 17 of the file.

Can be downloaded [here](https://www.data.gouv.fr/fr/datasets/base-carbone-complete-de-lademe-en-francais-v17-0/). 

Currently the system use OpenAI embeddings and OpenAI gpt3.5-turbo. It can be easily adapted to use any other LLM or embedding.

Note that a pure OpenAI implementation should use a ReAct Agent with appropriate SQL tools instead of a rag.

## install

Standard procedure, venv, requirements, you know the drill.

In addition you must create a `.env` file at the root of the project. To use OpenAI embeddings and/or model you'll need to add the following line to this file:
```
OPENAI_API_KEY=<your api key>
```

## Configure

The setings.yaml file already contains all the options like the name of files, model used, etc.

## Run the ETL

First step is to run the ETL to transform the excel file into a FAISS index.

```
python etl.py
```

For the ETL, we only need to change the embeddings if we want to adapt it to a non OpenAI solution. It's line 88.

```python
    faiss_index = FAISS.from_documents(documents, embedding=OpenAIEmbeddings())
```

## run the server

To run it locally:

```bash
uvicorn app.server:app --reload
```

When the server is started you can access the swagger documentation [here](http://127.0.0.1:8000/docs
)

## run the tests

```
pytest tests/
```
