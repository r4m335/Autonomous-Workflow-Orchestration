import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any

class VectorMemory:
    """
    Persistent shared memory across agents.
    Useful for entity resolution, caching previous decisions, and RAG over past workflows.
    """
    def __init__(self, persist_directory: str = "./chroma_data"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Collection for extracted entities (e.g. mapping unknown customer names to canonical IDs)
        self.entity_collection = self.client.get_or_create_collection(name="entities")
        
        # Collection for caching workflow decisions to optimize cost
        self.decision_collection = self.client.get_or_create_collection(name="decisions")

    def store_entity(self, entity_id: str, text: str, metadata: Dict[str, Any]):
        """Stores a resolved entity into vector memory."""
        self.entity_collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[entity_id]
        )

    def search_entities(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """Semantic search for entities to help the Validation/Decision agents normalize data."""
        results = self.entity_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # Reformat ChromaDB output for easier consumption
        matches = []
        if results and results.get("documents"):
            for i in range(len(results["documents"][0])):
                matches.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
        return matches

# Singleton instance
shared_memory = VectorMemory()
