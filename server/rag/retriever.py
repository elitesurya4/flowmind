from typing import Any, List, Dict

class FlowMindRetriever:
    def __init__(self, vectorstore: Any):
        """
        Initialize the retriever with a vectorstore.
        """
        self.vectorstore = vectorstore
        
    def retrieve(self, query: str) -> str:
        """
        Retrieve relevant documents for the given query.
        Returns a formatted string of relevant context.
        """
        docs = self.vectorstore.similarity_search(query, k=5)
        if not docs or all(not getattr(d, "page_content", None) for d in docs):
            return "No relevant documents found in the knowledge base."
        
        # Optionally, format context for LLM prompt
        context = "\n---\n".join(
            getattr(d, "page_content", str(d)) for d in docs if getattr(d, "page_content", None)
        )
        return context