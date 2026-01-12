import os
import logging
from typing import List
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


# --------------------------------------------------
# Environment & Logging
# --------------------------------------------------
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KNOWLEDGE_PATH = os.path.join(BASE_DIR, "knowledge_base")
VECTOR_DB_PATH = os.path.join(BASE_DIR, "vector_store")


class SecurityRAGEngine:
    """
    Production-grade RAG engine for IAM security knowledge
    """

    def __init__(self):
        self._validate_env()
        self.embeddings = OpenAIEmbeddings()
        self.vector_store: FAISS | None = None

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------
    def _validate_env(self):
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError("OPENAI_API_KEY not set")

        if not os.path.exists(KNOWLEDGE_PATH):
            raise FileNotFoundError("knowledge_base directory not found")

    # --------------------------------------------------
    # Knowledge Loading
    # --------------------------------------------------
    def _load_documents(self) -> List[Document]:
        documents = []

        files = [
            f for f in os.listdir(KNOWLEDGE_PATH)
            if f.endswith((".md", ".txt"))
        ]

        if not files:
            raise RuntimeError("No knowledge files found in knowledge_base")

        for file in files:
            file_path = os.path.join(KNOWLEDGE_PATH, file)
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append(
                    Document(
                        page_content=f.read(),
                        metadata={"source": file}
                    )
                )

        logger.info(f"Loaded {len(documents)} knowledge documents")
        return documents

    # --------------------------------------------------
    # Vector Store Build / Load
    # --------------------------------------------------
    def build_or_load_knowledge_base(self):
        """
        Load vector DB from disk if exists, else build it
        """
        if os.path.exists(VECTOR_DB_PATH):
            logger.info("Loading existing vector store")
            self.vector_store = FAISS.load_local(
                VECTOR_DB_PATH,
                self.embeddings,
                allow_dangerous_deserialization=False
            )
            return

        logger.info("Building new vector store")

        documents = self._load_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(documents)

        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.vector_store.save_local(VECTOR_DB_PATH)

        logger.info("Vector store built and saved")

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------
    def retrieve_context(self, query: str, k: int = 3) -> str:
        if not self.vector_store:
            raise RuntimeError("Vector store not initialized")

        docs = self.vector_store.similarity_search(
            query=query,
            k=k
        )

        return "\n\n".join(
            f"[Source: {doc.metadata.get('source')}]\n{doc.page_content}"
            for doc in docs
        )
