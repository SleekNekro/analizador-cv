import os
import qdrant_client
from llama_index.core import VectorStoreIndex, Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

def crear_indice(texto: str):
    client = qdrant_client.QdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=6333
    )

    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )

    Settings.llm = Ollama(
        model="qwen3:8b",
        base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        request_timeout=120.0
    )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name="cv_collection"
    )

    documento = Document(text=texto)
    indice = VectorStoreIndex.from_documents(
        [documento],
        vector_store=vector_store
    )
    return indice


def consultar_cv(indice, pregunta: str) -> str:
    query_engine = indice.as_query_engine()
    respuesta = query_engine.query(pregunta)
    return str(respuesta)