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

def test_pinecone_vector_store_add_texts():
    from unittest.mock import patch, MagicMock
    embedder = MockEmbedder()

    with patch('pinecone.Pinecone') as MockPinecone:
        mock_pc = MockPinecone.return_value
        mock_index = MagicMock()
        mock_pc.Index.return_value = mock_index

        # Initialize store
        store = PineconeVectorStore(index_name="test", embedder=embedder, api_key="fake-key")

        with patch('uuid.uuid4') as mock_uuid:
            mock_uuid.side_effect = [
                MagicMock(__str__=MagicMock(return_value="id-1")),
                MagicMock(__str__=MagicMock(return_value="id-2"))
            ]

            texts = ["doc 1", "doc 2"]
            metadatas = [{"source": "s1"}, {"source": "s2"}]

            ids = store.add_texts(texts, metadatas=metadatas)

            assert ids == ["id-1", "id-2"]
            mock_index.upsert.assert_called_once()

            upsert_args = mock_index.upsert.call_args[1]
            assert "vectors" in upsert_args
            vectors = upsert_args["vectors"]

            assert len(vectors) == 2

            # Embeddings of mock embedder are always [0.1, 0.2, 0.3]
            assert vectors[0] == {
                "id": "id-1",
                "values": [0.1, 0.2, 0.3],
                "metadata": {"source": "s1", "text": "doc 1"}
            }
            assert vectors[1] == {
                "id": "id-2",
                "values": [0.1, 0.2, 0.3],
                "metadata": {"source": "s2", "text": "doc 2"}
            }
