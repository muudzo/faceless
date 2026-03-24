import re

class ScriptGenerator:
    def __init__(self, max_length=150):
        self.max_length = max_length

    def generate_short_script(self, title, explanation):
        """
        Processes NASA APOD data into a short, punchy script.
        """
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
