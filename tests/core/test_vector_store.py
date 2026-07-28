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


def test_pinecone_vector_store_search(monkeypatch):
    import pinecone

    class MockIndex:
        def __init__(self, index_name):
            self.index_name = index_name

        def upsert(self, vectors):
            self.vectors = vectors

        def query(self, vector, top_k, include_metadata):
            return {
                'matches': [
                    {
                        'id': '123',
                        'score': 0.9,
                        'metadata': {'text': 'This is a test document', 'source': 'test'}
                    }
                ]
            }

    class MockPinecone:
        def __init__(self, api_key):
            self.api_key = api_key

        def Index(self, index_name):
            return MockIndex(index_name)

    monkeypatch.setattr(pinecone, "Pinecone", MockPinecone)

    embedder = MockEmbedder()
    store = PineconeVectorStore(index_name="test", embedder=embedder, api_key="test_api_key")

    results = store.search("test query", top_k=1)
    assert len(results) == 1
    assert results[0]["text"] == "This is a test document"
    assert results[0]["metadata"] == {"source": "test"}
    assert results[0]["score"] == 0.9
