from retrieval.retriever import (
    retrieve_papers
)

queries = [
    "low-data medical image classification transformers"
]

papers = retrieve_papers(
    queries
)

print(
    f"\nTotal Papers: {len(papers)}\n"
)

for paper in papers[:3]:

    print("=" * 50)

    print(
        "TITLE:",
        paper.get("title")
    )

    print(
        "YEAR:",
        paper.get("year")
    )

    print(
        "CITATIONS:",
        paper.get("citationCount")
    )

    print(
        "URL:",
        paper.get("url")
    )