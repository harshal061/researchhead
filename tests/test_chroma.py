from retrieval.retriever import (
    retrieve_papers
)

from vectorstore.chroma_manager import (
    add_papers_to_chroma,
    semantic_search
)

queries = [
    "low-data medical image classification transformers"
]

papers = retrieve_papers(
    queries
)

print(
    f"\nRetrieved {len(papers)} papers"
)

add_papers_to_chroma(
    papers
)

results = semantic_search(
    "few-shot vision transformers in medical imaging"
)

print("\nSEMANTIC RESULTS:\n")

for metadata in results[
    "metadatas"
][0]:

    print("=" * 50)

    print(
        "TITLE:",
        metadata["title"]
    )

    print(
        "YEAR:",
        metadata["year"]
    )

    print(
        "CITATIONS:",
        metadata["citations"]
    )