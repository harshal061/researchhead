from retrieval.retriever import (
    retrieve_papers
)

from retrieval.reranker import (
    rerank_results
)

queries = [
    "low-data medical image classification transformers"
]

papers = retrieve_papers(
    queries
)

results = rerank_results(
    "few-shot vision transformers medical imaging",
    papers
)

print("\nRERANKED RESULTS:\n")

for item in results:

    paper = item["paper"]

    print("=" * 50)

    print(
        "TITLE:",
        paper.get("title")
    )

    print(
        "SCORE:",
        round(
            item["score"],
            3
        )
    )