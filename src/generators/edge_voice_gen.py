import edge_tts
import asyncio
from pathlib import Path
from src.config import RAW_DATA_DIR

class EdgeVoiceGenerator:
    """
    Generator using Microsoft Edge-TTS for high-quality neural voices.
    """
    def __init__(self, voice="en-US-GuyNeural"):
        self.voice = voice

    async def _generate(self, text, output_path):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)

    def generate_voice(self, text, filename="voiceover_edge.mp3"):
        """
        Synchronous wrapper for the async edge-tts generation.
        """
        output_path = RAW_DATA_DIR / filename
        asyncio.run(self._generate(text, str(output_path)))
        return str(output_path)

if __name__ == "__main__":
    gen = EdgeVoiceGenerator()
    path = gen.generate_voice("Hello, this is a test of the Microsoft Edge neural voice system.")
    print(f"Voice generated at: {path}")
