from sentence_transformers import (
    CrossEncoder
)

from config import (
    RERANKER_MODEL
)

model = CrossEncoder(
    RERANKER_MODEL
)


def rerank_results(
    query,
    papers,
    top_k=10
):

    pairs = []

    for paper in papers:

        text = (
            paper.get("title", "")
            + " " +
            paper.get(
                "abstract",
                ""
            )
        )

        pairs.append(
            [query, text]
        )

    scores = model.predict(
        pairs
    )

    reranked = []

    for idx, paper in enumerate(
        papers
    ):

        reranked.append({

            "paper": paper,

            "score": float(
                scores[idx]
            )
        })

    reranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return reranked[:top_k]