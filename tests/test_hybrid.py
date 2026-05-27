from retrieval.retriever import (
    retrieve_papers
)

from vectorstore.chroma_manager import (
    add_papers_to_chroma
)

from retrieval.hybrid_search import (
    hybrid_search
)

queries = [
    "low-data medical image classification transformers"
]

papers = retrieve_papers(
    queries
)

add_papers_to_chroma(
    papers
)

results = hybrid_search(
    "few-shot vision transformers medical imaging",
    papers
)

print("\nHYBRID RESULTS:\n")

for item in results[:10]:

    print(item)