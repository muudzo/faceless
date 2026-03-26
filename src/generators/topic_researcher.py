from src.apis.groq_client import GroqClient
from src.apis.research_client import ResearchClient
from src.utils import setup_logger

logger = setup_logger()

class TopicResearcher:
    """
    Brainstorms and researches trending topics in the automation niche.
    """
    def __init__(self):
        self.ai = GroqClient()
        self.research = ResearchClient()

    def discover_topics(self, niche="Space Mysteries"):
        """
        Generates a list of trending or evergreen viral topics.
        """
        logger.info(f"Researching topics for niche: {niche}")
        prompt = f"""
        Generate 5 viral YouTube Shorts topic ideas for the '{niche}' niche.
        Focus on curiosity, mystery, and high-retention hooks.
        Return only the titles, separated by newlines.
        """
        try:
            raw_topics = self.ai.generate_content(prompt, system_prompt="You are a viral content strategist.")
            topics = [t.strip("- ").strip() for t in raw_topics.split("\n") if t.strip()]
            return topics[:5]
        except Exception as e:
            logger.error(f"Topic discovery failed: {e}")
            return ["The Fermi Paradox", "Voyager 1's Last Message", "Black Hole Anomalies"]

    def deep_research(self, topic):
        """
        Gathers facts and context for a specific topic.
        """
        logger.info(f"Performing deep research on: {topic}")
        wiki_data = self.research.search_and_verify(topic)
        
        # Use AI to synthesize research into a production brief
        prompt = f"Synthesize these facts into a 3-point curiosity brief for a video: {wiki_data['summary'] if wiki_data else 'General knowledge'}"
        brief = self.ai.generate_content(prompt, system_prompt="You are a research analyst.")
        
        return {
            "topic": topic,
            "brief": brief,
            "url": wiki_data['url'] if wiki_data else None
        }

if __name__ == "__main__":
    tr = TopicResearcher()
    topics = tr.discover_topics()
    print(f"Discovered: {topics}")
    if topics:
        brief = tr.deep_research(topics[0])
        print(f"Brief: {brief['brief']}")
