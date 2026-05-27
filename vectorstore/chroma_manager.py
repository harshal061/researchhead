import chromadb

from sentence_transformers import (
    SentenceTransformer
)

from config import (
    EMBEDDING_MODEL
)

client = chromadb.PersistentClient(
    path="./data/chroma_db"
)

collection = client.get_or_create_collection(
    name="research_papers"
)

model = SentenceTransformer(
    EMBEDDING_MODEL
)


def add_papers_to_chroma(
    papers
):

    documents = []
    ids = []
    metadatas = []

    for idx, paper in enumerate(papers):

        title = (
            paper.get("title") or ""
        )

        abstract = (
            paper.get("abstract") or ""
        )

        text = (
            title + " " + abstract
        )

        documents.append(text)

        ids.append(str(idx))

        metadatas.append({
            "title": title,
            "year": str(
                paper.get("year")
            ),
            "citations": str(
                paper.get(
                    "citationCount",
                    0
                )
            ),
            "url": paper.get("url")
        })

    embeddings = model.encode(
        documents
    ).tolist()

    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def semantic_search(
    query,
    top_k=5
):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results
def clear_collection():

    global collection

    client.delete_collection(
        "research_papers"
    )

    collection = (
        client.get_or_create_collection(
            name="research_papers"
        )
    )