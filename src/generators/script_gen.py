from src.apis.groq_client import GroqClient
from src.config import GROQ_API_KEY
import re

class ScriptGenerator:
    def __init__(self, max_length=500):
        self.max_length = max_length
        self.ai = None
        if GROQ_API_KEY:
            try:
                self.ai = GroqClient()
            except:
                pass

    async def generate_short_script(self, title, explanation, research_context=None):
        """
        Generates an engaging, emotional narrative using Llama-3 if available.
        """
        from src.utils import Sanitizer
        title = Sanitizer.clean_text(title)
        explanation = Sanitizer.clean_text(explanation)
        research_context = Sanitizer.clean_text(research_context) if research_context else None

        if self.ai:
            prompt = f"""
            Write a viral, emotional 60-second YouTube Shorts script about {title}.
            NASA Fact: {explanation}
            {f'Expert Context: {research_context}' if research_context else ''}
            
            Rules:
            1. Start with a massive hook.
            2. Use 'You' to engage the audience.
            3. End with a question or call to action.
            4. Keep it under 140 words.
            """
            try:
                script = await self.ai.generate_content(prompt, system_prompt="You are a viral YouTube storyteller.")
                return script.strip()
            except:
                pass

        # Fallback to basic cleaning logic
        # Clean up the explanation (remove parenthetical citations, excessive spaces)
        clean_text = re.sub(r'\([^)]*\)', '', explanation)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?]) +', clean_text)
        
        # Take the first few sentences that fit within max_length
        script_parts = [f"Did you know about {title}?"]
        current_len = len(script_parts[0])
        
        for sentence in sentences:
            if current_len + len(sentence) + 1 <= self.max_length:
                script_parts.append(sentence)
                current_len += len(sentence) + 1
            else:
                break
        
        script_parts.append("Fascinating, isn't it? Subscribe for more daily cosmic curiosities.")
        
        return " ".join(script_parts)

if __name__ == "__main__":
    generator = ScriptGenerator()
    test_title = "The Orion Nebula"
    test_explanation = "The Orion Nebula (also known as Messier 42, M42, or NGC 1976) is a diffuse nebula situated in the Milky Way, being south of Orion's Belt in the constellation of Orion. It is one of the brightest nebulae and is visible to the naked eye in the night sky. M42 is located at a distance of 1,344 (plus or minus 20) light years and is the closest region of massive star formation to Earth."
    
    script = generator.generate_short_script(test_title, test_explanation)
    print(f"Generated Script: {script}")
