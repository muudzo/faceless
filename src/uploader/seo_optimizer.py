import requests
import json
from src.utils import setup_logger, retry

logger = setup_logger()

class SEOOptimizer:
    """
    Optimizes video SEO by scraping YouTube autocomplete suggestions.
    """
    def __init__(self):
        self.base_url = "http://suggestqueries.google.com/complete/search"

    @retry(Exception, tries=3, delay=2)
    def get_suggestions(self, query):
        """
        Gets YouTube search suggestions for a query.
        """
        params = {
            "client": "youtube",
            "ds": "yt",
            "q": query,
            "hl": "en"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(self.base_url, params=params, headers=headers)
        if response.status_code == 200:
            # Response format: window.google.ac.h(["query", [["suggestion1", 0], ["suggestion2", 0], ...], {"q": "..."}])
            # Or similar JSON-like structure. Basic cleaning needed.
            try:
                # The response is usually a list-like string
                data = response.text
                start = data.find("(")
                end = data.rfind(")")
                json_data = json.loads(data[start+1:end])
                suggestions = [s[0] for s in json_data[1]]
                return suggestions
            except Exception as e:
                logger.warning(f"Failed to parse suggestions: {e}")
                return []
        return []

    def optimize_metadata(self, topic):
        """
        Returns optimized titles and tags based on suggestions.
        """
        suggestions = self.get_suggestions(topic)
        logger.info(f"SEO suggestions for {topic}: {suggestions}")
        
        # Primary title is usually the first/top suggestion
        best_title = suggestions[0] if suggestions else topic
        tags = suggestions[:10] # Top 10 as tags
        
        return {
            "title": best_title,
            "tags": tags,
            "suggestions": suggestions
        }

if __name__ == "__main__":
    seo = SEOOptimizer()
    res = seo.optimize_metadata("Space Facts")
    print(res)
