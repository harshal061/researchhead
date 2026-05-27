import streamlit as st

from agents.intent_agent import (
    extract_intent
)

from retrieval.retriever import (
    retrieve_papers
)

from vectorstore.chroma_manager import (
    add_papers_to_chroma,clear_collection
)

from retrieval.hybrid_search import (
    hybrid_search
)

from retrieval.reranker import (
    rerank_results
)

st.set_page_config(
    page_title="ResearchHead",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 ResearchHead")

st.markdown(
    """
AI-powered academic research copilot
with hybrid semantic retrieval.
"""
)

query = st.text_area(
    "Enter Research Problem",
    height=150
)

if st.button("Search Papers"):

    if not query.strip():

        st.warning(
            "Please enter a query."
        )

        st.stop()

    with st.spinner(
        "Extracting intent..."
    ):

        intent = extract_intent(
            query
        )

    st.subheader(
        "Detected Intent"
    )

    st.json(intent)

    with st.spinner(
        "Retrieving papers..."
    ):

        retrieval_queries = [
    intent["core_problem"]
]

    retrieval_queries.extend(
        intent["expanded_queries"][:2]
    )

    papers = retrieve_papers(
        retrieval_queries
    )

    with st.spinner(
        "Building semantic index..."
    ):
        clear_collection()
        add_papers_to_chroma(
            papers
        )

    with st.spinner(
        "Performing hybrid retrieval..."
    ):

        hybrid_results = (
            hybrid_search(
                query,
                papers
            )
        )

    title_to_paper = {}

    for paper in papers:

        title_to_paper[
            paper["title"]
        ] = paper

    rerank_candidates = []

    for item in hybrid_results:

        title = item[0]

        if title in title_to_paper:

            rerank_candidates.append(
                title_to_paper[
                    title
                ]
            )

    with st.spinner(
        "Reranking results..."
    ):

        final_results = (
            rerank_results(
                query,
                rerank_candidates
            )
        )

    st.subheader(
        "Top Research Papers"
    )

    for idx, result in enumerate(
        final_results,
        start=1
    ):

        paper = result["paper"]

        score = result["score"]

        with st.container(
            border=True
        ):

            st.markdown(
                f"## {idx}. {paper.get('title')}"
            )

            st.write(
                f"### Relevance Score: {round(score, 3)}"
            )

            st.write(
                f"**Year:** {paper.get('year')}"
            )

            st.write(
                f"**Citations:** {paper.get('citationCount')}"
            )
            st.write(
                f"**Source:** {paper.get('source')}"
            )

            abstract = (
                paper.get(
                    "abstract",
                    "No abstract available."
                )
            )
            if abstract.strip():

                st.markdown("### Abstract")

                st.write(
                    abstract[:500]
                )

               

            st.markdown(
                f"[Open Paper]({paper.get('url')})"
            )