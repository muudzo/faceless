from src.apis.groq_client import GroqClient
from src.utils import setup_logger

logger = setup_logger()

class StoryEngine:
    """
    Generates high-retention story scripts using psychological hooks.
    """
    def __init__(self):
        self.ai = GroqClient()

    def generate_betrayal_story(self, topic="A business partner"):
        """
        Creates a 'Betrayal' narrative with a cliffhanger.
        """
        prompt = f"""
        Write a 60-second YouTube Shorts script about a betrayal involving {topic}.
        
        Structure:
        1. The Hook: Something shocking happened.
        2. The Build-up: How they trusted them.
        3. The Twist: The moment of betrayal.
        4. The Resolution/Cliffhanger: What happened next.
        
        Style: Tense, fast-paced, high emotion.
        Length: < 150 words.
        """
        try:
            story = self.ai.generate_content(prompt, system_prompt="You are a master of psychological thrillers.")
            return story.strip()
        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            return f"He thought he could trust his partner, but {topic} had a darker plan..."

if __name__ == "__main__":
    se = StoryEngine()
    story = se.generate_betrayal_story("a secret inheritance")
    print(story)
