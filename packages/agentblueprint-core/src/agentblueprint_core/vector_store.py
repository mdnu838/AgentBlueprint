"""
Vector database interfaces and implementations for knowledge retrieval.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class Embedder(ABC):
    """Abstract base class for text embedding."""

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of document strings."""
        pass

class VectorStore(ABC):
    """Abstract base class for vector databases."""

    @abstractmethod
    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a text document and return its ID."""
        pass

    @abstractmethod
    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        """Add multiple text documents and return their IDs."""
        pass

    @abstractmethod
    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        Returns a list of dicts with 'text', 'metadata', and 'score' keys.
        """
        pass

class ChromaVectorStore(VectorStore):
    """VectorStore implementation using ChromaDB."""

    def __init__(self, collection_name: str = "default", persist_directory: Optional[str] = None, embedder: Optional[Embedder] = None):
        try:
            import chromadb
        except ImportError:
            raise ImportError("chromadb is required. Install with `pip install chromadb`.")

        if persist_directory:
            self.client = chromadb.PersistentClient(path=persist_directory)
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = embedder

    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        return self.add_texts([text], [metadata] if metadata else None)[0]

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        if not texts:
            return []

        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]
        embeddings = self.embedder.embed_documents(texts) if self.embedder else None

        batch_size = self.client.get_max_batch_size()

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]

            # Extract metadata and embeddings for the batch
            batch_metadatas = metadatas[i:i + batch_size] if metadatas else [{} for _ in batch_texts]

            add_kwargs = {
                "documents": batch_texts,
                "metadatas": batch_metadatas,
                "ids": batch_ids
            }

            if embeddings:
                add_kwargs["embeddings"] = embeddings[i:i + batch_size]

            self.collection.add(**add_kwargs)

        return ids

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        query_kwargs = {"n_results": top_k}
        if self.embedder:
            query_kwargs["query_embeddings"] = [self.embedder.embed_query(query)]
        else:
            query_kwargs["query_texts"] = [query]

        results = self.collection.query(**query_kwargs)

        output = []
        if results['documents'] and len(results['documents']) > 0:
            docs = results['documents'][0]
            metadatas = results['metadatas'][0] if results['metadatas'] else [{} for _ in docs]
            distances = results['distances'][0] if results['distances'] else [0.0 for _ in docs]

            for doc, meta, dist in zip(docs, metadatas, distances):
                output.append({
                    "text": doc,
                    "metadata": meta,
                    "score": 1.0 / (1.0 + dist)  # rough distance to similarity score
                })
        return output

class QdrantVectorStore(VectorStore):
    """VectorStore implementation using Qdrant."""

    def __init__(self, collection_name: str, embedder: Embedder, url: Optional[str] = None, path: Optional[str] = None):
        try:
            from qdrant_client import QdrantClient
        except ImportError:
            raise ImportError("qdrant-client is required. Install with `pip install qdrant-client`.")

        if url:
            self.client = QdrantClient(url=url)
        elif path:
            self.client = QdrantClient(path=path)
        else:
            self.client = QdrantClient(":memory:")

        self.collection_name = collection_name
        self.embedder = embedder

    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        return self.add_texts([text], [metadata] if metadata else None)[0]

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        from qdrant_client.models import PointStruct
        import uuid

        ids = [str(uuid.uuid4()) for _ in texts]
        embeddings = self.embedder.embed_documents(texts)

        points = []
        for i, (text, emb) in enumerate(zip(texts, embeddings)):
            payload = metadatas[i] if metadatas else {}
            payload['text'] = text
            points.append(PointStruct(id=ids[i], vector=emb, payload=payload))

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        return ids

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        query_emb = self.embedder.embed_query(query)
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_emb,
            limit=top_k
        ).points

        output = []
        for match in results:
            payload = match.payload or {}
            text = payload.pop('text', '')
            output.append({
                "text": text,
                "metadata": payload,
                "score": match.score
            })
        return output

class PineconeVectorStore(VectorStore):
    """VectorStore implementation using Pinecone."""

    def __init__(self, index_name: str, embedder: Embedder, api_key: Optional[str] = None):
        try:
            from pinecone import Pinecone
        except ImportError:
            raise ImportError("pinecone is required. Install with `pip install pinecone`.")

        import os
        api_key = api_key or os.environ.get("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("Pinecone API key is required.")

        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index(index_name)
        self.embedder = embedder

    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        return self.add_texts([text], [metadata] if metadata else None)[0]

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> List[str]:
        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]
        embeddings = self.embedder.embed_documents(texts)

        vectors = []
        for i, (text, emb) in enumerate(zip(texts, embeddings)):
            meta = metadatas[i] if metadatas else {}
            meta['text'] = text
            vectors.append({"id": ids[i], "values": emb, "metadata": meta})

        self.index.upsert(vectors=vectors)
        return ids

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        query_emb = self.embedder.embed_query(query)
        results = self.index.query(vector=query_emb, top_k=top_k, include_metadata=True)

        output = []
        for match in results['matches']:
            meta = match.get('metadata', {})
            text = meta.pop('text', '')
            output.append({
                "text": text,
                "metadata": meta,
                "score": match.get('score', 0.0)
            })
        return output
