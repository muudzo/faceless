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

    async def search_and_verify(self, topic):
        """
        Searches for a topic and returns a summary for verification.
        """
        from src.utils import Sanitizer
        topic = Sanitizer.clean_text(topic)
        
        import anyio
        def _sync_wiki():
            page = self.wiki.page(topic)
            if page.exists():
                return {
                    "title": page.title,
                    "summary": page.summary[0:1000],  # First 1000 characters
                    "url": page.fullurl
                }
            return None
            
        return await anyio.to_thread.run_sync(_sync_wiki)

if __name__ == "__main__":
    client = ResearchClient()
    result = client.search_and_verify("Mars")
    if result:
        print(f"Verified: {result['title']}")
    else:
        print("Topic not found.")
