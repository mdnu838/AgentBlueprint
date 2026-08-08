import pytest
from typing import List
from agentblueprint_core.vector_store import (
    Embedder,
    VectorStore,
    ChromaVectorStore,
    PineconeVectorStore,
    QdrantVectorStore
)

class MockEmbedder(Embedder):
    def embed_query(self, text: str) -> List[float]:
        return [0.1, 0.2, 0.3]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]

def test_chroma_vector_store():
    # Test Chroma with in-memory client
    store = ChromaVectorStore(collection_name="test_collection")

    # Test add
    doc_id = store.add("This is a test document", metadata={"source": "test"})
    assert isinstance(doc_id, str)

    # Test search
    results = store.search("test", top_k=1)
    assert len(results) == 1
    assert results[0]["text"] == "This is a test document"
    assert results[0]["metadata"] == {"source": "test"}
    assert "score" in results[0]

def test_chroma_vector_store_empty_texts():
    store = ChromaVectorStore(collection_name="test_empty_collection")
    result = store.add_texts([])
    assert result == []

def test_chroma_vector_store_batching(monkeypatch):
    import unittest.mock

    store = ChromaVectorStore(collection_name="test_batch_collection")

    # Mock the client's get_max_batch_size to a small number
    monkeypatch.setattr(store.client, 'get_max_batch_size', lambda: 2)

    # Add 5 items, which should result in 3 batches (2, 2, 1)
    texts = ["doc1", "doc2", "doc3", "doc4", "doc5"]
    metadatas = [{"id": i} for i in range(5)]

    # Spy on the collection add method
    original_add = store.collection.add
    spy = unittest.mock.MagicMock(side_effect=original_add)
    monkeypatch.setattr(store.collection, 'add', spy)

    result = store.add_texts(texts, metadatas=metadatas)

    assert len(result) == 5
    assert spy.call_count == 3

    # Verify the first call has 2 documents
    first_call_args = spy.call_args_list[0].kwargs
    assert len(first_call_args["documents"]) == 2

    # Verify search still works for these batched documents
    results = store.search("doc1", top_k=5)
    assert len(results) == 5

def test_qdrant_vector_store():
    embedder = MockEmbedder()
    # Test Qdrant with in-memory client. For memory, we must create collection first.
    store = QdrantVectorStore(collection_name="test_collection", embedder=embedder)
    from qdrant_client.models import VectorParams, Distance
    store.client.create_collection(
        collection_name="test_collection",
        vectors_config=VectorParams(size=3, distance=Distance.COSINE),
    )

    # Test add
    doc_id = store.add("This is a test document", metadata={"source": "test"})
    assert isinstance(doc_id, str)

    # Test search
    results = store.search("test", top_k=1)
    assert len(results) == 1
    assert results[0]["text"] == "This is a test document"
    assert results[0]["metadata"] == {"source": "test"}
    assert "score" in results[0]

# Testing Pinecone requires API keys and network calls, so we'd typically mock it completely
# For this example, we skip actual Pinecone tests unless mocked, but we can test initialization errors.
def test_pinecone_init_error():
    embedder = MockEmbedder()
    with pytest.raises(ValueError, match="Pinecone API key is required"):
        # Without setting PINECONE_API_KEY env var
        PineconeVectorStore(index_name="test", embedder=embedder)
