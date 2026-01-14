from typing import Any, List, Dict
import json
from collections import Counter
import ast

class FlowMindRetriever:
    def __init__(self, vectorstore: Any):
        """
        Initialize the retriever with a vectorstore.
        """
        self.vectorstore = vectorstore
        
    def retrieve(self, query: str) -> str:
        """
        Two-phase regulatory SOP chain resolver.
        """

        # PHASE 1 — discover SOP family semantically
        probes = self.vectorstore.similarity_search(query, k=50)

        if not probes:
            return "No SOP content found."

        use_cases = []
        for d in probes:
            try:
                content = d.page_content
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError:
                        content = ast.literal_eval(content)
                use_cases.append(content.get('use_case', ""))
            except Exception:
                continue

        unique_use_cases = set(use_cases)
        print(f"Unique use_cases found: {len(unique_use_cases)} - {unique_use_cases}")  # Debug info

        if not use_cases:
            return "No SOP family detected."

        # Most semantically relevant SOP family
        use_case = Counter(use_cases).most_common(1)[0][0]

        # PHASE 2 — load FULL chain for this SOP family

        chain = []
        for use_case in unique_use_cases:
            all_docs = self.vectorstore.similarity_search(use_case, k=300)
            for d in all_docs:
                try:
                    content = d.page_content
                    if isinstance(content, str):
                        try:
                            obj = json.loads(content)
                        except json.JSONDecodeError:
                            content = ast.literal_eval(content)
                            obj = content
                    else:
                        obj = content
                    if obj["use_case"] == use_case or obj["use_case"] == "generic":
                        chain.append(obj)
                except:
                    continue

        if not chain:
            return "No SOP chain resolved."

        # Deterministic regulatory ordering
        chain = sorted(chain, key=lambda x: x["step_order"])

        return json.dumps(chain, indent=2)