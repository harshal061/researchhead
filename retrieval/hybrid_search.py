from rank_bm25 import BM25Okapi

from vectorstore.chroma_manager import (
    semantic_search
)


def reciprocal_rank_fusion(
    rankings,
    k=60
):

    scores = {}

    for ranking in rankings:

        for rank, paper in enumerate(ranking):

            title = paper["title"]

            scores[title] = (
                scores.get(title, 0)
                + 1 / (k + rank + 1)
            )

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


def hybrid_search(
    query,
    papers,
    top_k=10
):

    corpus = []

    for paper in papers:

        text = (
            paper.get("title", "")
            + " " +
            paper.get(
                "abstract",
                ""
            )
        )

        corpus.append(text)

    tokenized_corpus = [
        doc.lower().split()
        for doc in corpus
    ]

    bm25 = BM25Okapi(
        tokenized_corpus
    )

    tokenized_query = (
        query.lower().split()
    )

    bm25_scores = bm25.get_scores(
        tokenized_query
    )

    bm25_ranked = sorted(
        zip(papers, bm25_scores),
        key=lambda x: x[1],
        reverse=True
    )

    bm25_ranked = [
        x[0]
        for x in bm25_ranked[:top_k]
    ]

    semantic_results = semantic_search(
        query,
        top_k=top_k
    )

    semantic_ranked = []

    for metadata in semantic_results[
        "metadatas"
    ][0]:

        semantic_ranked.append({
            "title":
            metadata["title"],

            "year":
            metadata["year"],

            "citationCount":
            metadata["citations"],

            "url":
            metadata["url"]
        })

    fused = reciprocal_rank_fusion([
        bm25_ranked,
        semantic_ranked
    ])

    return fused