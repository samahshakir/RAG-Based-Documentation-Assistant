import chromadb
import os

class ChromaDBManager:
    """
    Manages the initialization and interaction with a local ChromaDB instance.
    """
    def __init__(self, db_path: str = "./chroma_data", collection_name: str = "documentation_embeddings"):
        """
        Initializes the ChromaDB client and ensures the collection exists.

        Args:
            db_path (str): The path where ChromaDB will store its data.
                           Defaults to './chroma_data'.
            collection_name (str): The name of the collection to use or create.
                                   Defaults to 'documentation_embeddings'.
        """
        self.db_path = os.path.abspath(db_path)
        self.collection_name = collection_name
        self.client = self._initialize_client()
        self.collection = self._get_or_create_collection()
        print(f"ChromaDB Manager initialized. DB Path: {self.db_path}, Collection: {self.collection_name}")

    def _initialize_client(self) -> chromadb.Client:
        """
        Initializes a persistent ChromaDB client.
        """
        print(f"Initializing ChromaDB client at {self.db_path}...")
        return chromadb.PersistentClient(path=self.db_path)

    def _get_or_create_collection(self) -> chromadb.Collection:
        """
        Gets an existing collection or creates a new one if it doesn't exist.
        """
        print(f"Getting or creating collection '{self.collection_name}'...")
        return self.client.get_or_create_collection(name=self.collection_name)

    def get_collection(self) -> chromadb.Collection:
        """
        Returns the initialized ChromaDB collection.
        """
        return self.collection

    def add_documents(self, documents: list[str], metadatas: list[dict], ids: list[str]):
        """
        Adds documents, their metadata, and unique IDs to the collection.

        Args:
            documents (list[str]): A list of text documents to add.
            metadatas (list[dict]): A list of metadata dictionaries, one per document.
            ids (list[str]): A list of unique string IDs for each document.
        """
        print(f"Adding {len(documents)} documents to collection '{self.collection_name}'...")
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Successfully added {len(documents)} documents.")

    def query_documents(self, query_texts: list[str], n_results: int = 5) -> dict:
        """
        Queries the collection for similar documents.

        Args:
            query_texts (list[str]): A list of query strings.
            n_results (int): The number of results to return for each query.

        Returns:
            dict: The query results from ChromaDB.
        """
        print(f"Querying collection '{self.collection_name}' for '{query_texts}' (top {n_results} results)...")
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results
        )
        return results

# Example Usage (for demonstration and testing)
if __name__ == "__main__":
    # Ensure the chroma_data directory is clean for a fresh run
    import shutil
    if os.path.exists("./chroma_data"):
        print("Cleaning up existing ./chroma_data directory...")
        shutil.rmtree("./chroma_data")

    # 1. Initialize the ChromaDB Manager
    db_manager = ChromaDBManager(db_path="./chroma_data", collection_name="company_docs")

    # 2. Add some documents
    docs_to_add = [
        "The first quarter financial report shows strong growth in SaaS subscriptions.",
        "Our new employee onboarding process includes a mandatory security awareness training.",
        "The API documentation for version 2.1 introduces several breaking changes.",
        "Customer support response times have improved significantly after implementing the new ticketing system."
    ]
    metadatas_to_add = [
        {"source": "Q1_Report.pdf", "page": 5, "department": "finance"},
        {"source": "HR_Handbook.pdf", "section": "onboarding", "department": "HR"},
        {"source": "API_Docs_v2.1.md", "version": "2.1", "department": "engineering"},
        {"source": "CS_Report.pdf", "quarter": "Q2", "department": "customer_service"}
    ]
    ids_to_add = [f"doc{i}" for i in range(len(docs_to_add))]

    db_manager.add_documents(documents=docs_to_add, metadatas=metadatas_to_add, ids=ids_to_add)

    # 3. Query the documents
    query = ["How can I learn about the new API features?"]
    results = db_manager.query_documents(query_texts=query, n_results=2)

    print("\nQuery Results:")
    for i in range(len(results['documents'][0])):
        print(f"  Document: {results['documents'][0][i]}")
        print(f"  Metadata: {results['metadatas'][0][i]}")
        print(f"  Distance: {results['distances'][0][i]:.4f}")
        print("  ---")

    query_hr = ["What is the process for new hires?"]
    results_hr = db_manager.query_documents(query_texts=query_hr, n_results=1)

    print("\nQuery Results (HR):")
    for i in range(len(results_hr['documents'][0])):
        print(f"  Document: {results_hr['documents'][0][i]}")
        print(f"  Metadata: {results_hr['metadatas'][0][i]}")
        print(f"  Distance: {results_hr['distances'][0][i]:.4f}")
        print("  ---")
