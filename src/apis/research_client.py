import wikipediaapi
from src.utils import retry

class ResearchClient:
    """
    Client for interacting with Wikipedia for fact-checking and research.
    """
    def __init__(self, user_agent="CosmicCuriosities/1.0 (contact@example.com)"):
        self.wiki = wikipediaapi.Wikipedia(
            user_agent=user_agent,
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )

    @retry(Exception, tries=2, delay=1)
    def search_and_verify(self, topic):
        """
        Searches for a topic and returns a summary for verification.
        """
        page = self.wiki.page(topic)
        if page.exists():
            return {
                "title": page.title,
                "summary": page.summary[0:1000],  # First 1000 characters
                "url": page.fullurl
            }
        return None

if __name__ == "__main__":
    client = ResearchClient()
    result = client.search_and_verify("Mars")
    if result:
        print(f"Verified: {result['title']}")
    else:
        print("Topic not found.")
