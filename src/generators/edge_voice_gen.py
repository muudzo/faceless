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

    async def generate_voice(self, text, filename="voiceover_edge.mp3", session_dir=None):
        """
        Asynchronous voice generation.
        """
        output_path = (Path(session_dir) if session_dir else RAW_DATA_DIR) / filename
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(str(output_path))
        return str(output_path)

if __name__ == "__main__":
    gen = EdgeVoiceGenerator()
    path = gen.generate_voice("Hello, this is a test of the Microsoft Edge neural voice system.")
    print(f"Voice generated at: {path}")
