import requests
import feedparser
from urllib.parse import quote

SEMANTIC_SCHOLAR_URL = (
    "https://api.semanticscholar.org/graph/v1/paper/search"
)

OPENALEX_URL = (
    "https://api.openalex.org/works"
)

ARXIV_URL = (
    "http://export.arxiv.org/api/query"
)


def search_semantic_scholar(
    query,
    limit=20
):

    try:

        params = {
            "query": query,
            "limit": limit,
            "fields":
            "title,abstract,year,citationCount,url"
        }

        response = requests.get(
            SEMANTIC_SCHOLAR_URL,
            params=params,
            timeout=20
        )

        data = response.json()

        papers = []

        for item in data.get("data", []):

            papers.append({

                "title":
                item.get("title"),

                "abstract":
                item.get("abstract"),

                "year":
                item.get("year"),

                "citationCount":
                item.get(
                    "citationCount",
                    0
                ),

                "url":
                item.get("url"),

                "source":
                "Semantic Scholar"
            })

        return papers

    except Exception as e:

        print(
            "Semantic Scholar Error:",
            e
        )

        return []

def search_openalex(
    query,
    limit=20
):

    try:

        params = {
            "search": query,
            "per-page": limit
        }

        response = requests.get(
            OPENALEX_URL,
            params=params,
            timeout=20
        )

        data = response.json()

        papers = []

        for item in data.get(
            "results",
            []
        ):

            papers.append({
                "title":
                item.get("title"),

                "abstract":
                "",

                "year":
                item.get(
                    "publication_year"
                ),

                "citationCount":
                item.get(
                    "cited_by_count",
                    0
                ),
                
                "url":
                item.get("id"),

                "source": 
                "OpenAlex"
            })

        return papers

    except Exception as e:

        print(
            "OpenAlex Error:",
            e
        )

        return []


def search_arxiv(
    query,
    limit=20
):

    try:

        encoded_query = quote(query)

        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=all:{encoded_query}"
            f"&start=0"
            f"&max_results={limit}"
        )

        feed = feedparser.parse(url)

        papers = []

        for entry in feed.entries:

            papers.append({

                "title":
                entry.title,

                "abstract":
                entry.summary,

                "year":
                entry.published[:4],

                "citationCount":
                0,

                "url":
                entry.link,

                "source": 
                "arXiv"
            })

        return papers

    except Exception as e:

        print(
            "arXiv Error:",
            e
        )

        return []
def deduplicate_papers(
    papers
):

    seen = set()

    unique = []

    for paper in papers:

        title = (
            paper.get("title", "")
            .lower()
            .strip()
        )

        if title not in seen:

            seen.add(title)

            unique.append(paper)

    return unique
def retrieve_papers(
    queries
):

    all_papers = []

    for idx,query in enumerate(queries):
        limit = 25 if idx == 0 else 8
        semantic_results = (
            search_semantic_scholar(query,limit=12)
        )

        openalex_results = (
            search_openalex(query,limit=6)
        )

        arxiv_results = (
            search_arxiv(query,limit=10)
        )

        all_papers.extend(
            semantic_results
        )

        all_papers.extend(
            openalex_results
        )

        all_papers.extend(
            arxiv_results
        )

    return deduplicate_papers(
    all_papers
)