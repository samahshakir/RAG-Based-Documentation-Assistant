import os
from abc import ABC, abstractmethod
from pathlib import Path

# --- Configuration ---
LOCAL_STORAGE_BASE_DIR = os.getenv("LOCAL_STORAGE_BASE_DIR", "./data/documents")


# --- Interface Definition ---
class DocumentStorage(ABC):
    """Abstract Base Class for document storage solutions."""

    @abstractmethod
    def save_document(self, content: bytes, filename: str) -> str:
        """Saves document content to storage. Returns the stored filename."""
        pass

    @abstractmethod
    def get_document_content(self, filename: str) -> bytes:
        """Retrieves document content by filename."""
        pass

    @abstractmethod
    def get_document_path(self, filename: str) -> str:
        """Returns the absolute path to a document if stored locally, or a reference if cloud-based."""
        pass

    @abstractmethod
    def list_documents(self) -> list[str]:
        """Lists all stored document filenames."""
        pass

    @abstractmethod
    def document_exists(self, filename: str) -> bool:
        """Checks if a document with the given filename exists."""
        pass

    @abstractmethod
    def delete_document(self, filename: str) -> bool:
        """Deletes a document by filename. Returns True if successful, False otherwise."""
        pass


# --- Local Storage Implementation ---
class LocalDocumentStorage(DocumentStorage):
    """Concrete implementation of DocumentStorage for local file system."""

    def __init__(self, base_directory: str = LOCAL_STORAGE_BASE_DIR):
        self.base_path = Path(base_directory).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_full_path(self, filename: str) -> Path:
        """Helper to get the full path for a given filename within the base directory."""
        # Ensure filename does not contain path traversals
        relative_filename = Path(filename).name
        return self.base_path / relative_filename

    def save_document(self, content: bytes, filename: str) -> str:
        full_path = self._get_full_path(filename)
        try:
            with open(full_path, "wb") as f:
                f.write(content)
            return filename
        except IOError as e:
            raise IOError(f"Failed to save document '{filename}': {e}")

    def get_document_content(self, filename: str) -> bytes:
        full_path = self._get_full_path(filename)
        if not full_path.is_file():
            raise FileNotFoundError(f"Document '{filename}' not found at {full_path}")
        try:
            with open(full_path, "rb") as f:
                return f.read()
        except IOError as e:
            raise IOError(f"Failed to read document '{filename}': {e}")

    def get_document_path(self, filename: str) -> str:
        full_path = self._get_full_path(filename)
        if not full_path.is_file():
            raise FileNotFoundError(f"Document '{filename}' not found at {full_path}")
        return str(full_path)

    def list_documents(self) -> list[str]:
        return [p.name for p in self.base_path.iterdir() if p.is_file()]

    def document_exists(self, filename: str) -> bool:
        return self._get_full_path(filename).is_file()

    def delete_document(self, filename: str) -> bool:
        full_path = self._get_full_path(filename)
        if full_path.is_file():
            try:
                os.remove(full_path)
                return True
            except OSError as e:
                print(f"Error deleting document '{filename}': {e}")
                return False
        return False

# Example Usage (optional, for demonstration)
if __name__ == "__main__":
    print(f"Initializing LocalDocumentStorage in {LOCAL_STORAGE_BASE_DIR}")
    storage = LocalDocumentStorage()

    # Test saving a document
    test_content_1 = b"This is the content of document one."
    test_filename_1 = "doc_one.txt"
    storage.save_document(test_content_1, test_filename_1)
    print(f"Saved: {test_filename_1}")

    test_content_2 = b"Another document with different content."
    test_filename_2 = "another_doc.md"
    storage.save_document(test_content_2, test_filename_2)
    print(f"Saved: {test_filename_2}")

    # Test listing documents
    print("\nDocuments in storage:", storage.list_documents())

    # Test checking existence
    print(f"Does {test_filename_1} exist? {storage.document_exists(test_filename_1)}")
    print(f"Does non_existent_doc.txt exist? {storage.document_exists('non_existent_doc.txt')}")

    # Test retrieving content
    retrieved_content = storage.get_document_content(test_filename_1)
    print(f"\nContent of {test_filename_1}: {retrieved_content.decode()}")

    # Test getting path
    doc_path = storage.get_document_path(test_filename_2)
    print(f"Path of {test_filename_2}: {doc_path}")

    # Test deleting a document
    print(f"\nDeleting {test_filename_1}...")
    if storage.delete_document(test_filename_1):
        print(f"{test_filename_1} deleted successfully.")
    else:
        print(f"Failed to delete {test_filename_1}.")

    print("Documents after deletion:", storage.list_documents())

    # Clean up (optional, for example to remove the base directory after tests)
    # import shutil
    # if os.path.exists(LOCAL_STORAGE_BASE_DIR):
    #     print(f"\nCleaning up directory: {LOCAL_STORAGE_BASE_DIR}")
    #     shutil.rmtree(LOCAL_STORAGE_BASE_DIR)
