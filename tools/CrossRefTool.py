from crewai.tools import BaseTool
import requests
from typing import List
import logging

logger = logging.getLogger(__name__)

class CrossRefTool(BaseTool):
    name: str = "CrossRef API Tool"
    description: str = "Fetch articles from the CrossRef API using a search query."

    def _run(self, query: str, rows: int = 5) -> List[dict]:
        logger.info(f"Searching CrossRef for query: '{query}'")
        url = "https://api.crossref.org/works"
        params = {
            "query": query,
            "rows": rows,
            "filter": "type:journal-article",
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            logger.error(f"CrossRef API request failed: {e}")
            return []

        return [
            {
                "title": item.get("title", ["No title"])[0],
                "authors": ", ".join(f"{a.get('given', '')} {a.get('family', '')}".strip() for a in item.get("author", [])) or "N/A",
                "published": (
                    (item.get("published-print") or item.get("published-online") or {})
                    .get("date-parts", [[None]])[0][0]
                ),
                "URL": item.get("URL", "#"),
                "summary": item.get("abstract", "No summary available")
            }
            for item in data.get("message", {}).get("items", [])
        ]
