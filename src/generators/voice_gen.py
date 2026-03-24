from gtts import gTTS
import os
from src.config import PROCESSED_DATA_DIR, VOICE_LANGUAGE, VOICE_SLOW

class VoiceGenerator:
    def __init__(self, lang=VOICE_LANGUAGE, slow=VOICE_SLOW):
        self.lang = lang
        self.slow = slow

    def generate_voice(self, text, filename="voiceover.mp3"):
        """
        Generates an MP3 file from text using gTTS.
        """
        tts = gTTS(text=text, lang=self.lang, slow=self.slow)
        save_path = PROCESSED_DATA_DIR / filename
        tts.save(str(save_path))
        return str(save_path)

if __name__ == "__main__":
    generator = VoiceGenerator()
    test_text = "This is a test of the cosmic curiosities voiceover system. Checking one, two, three."
    path = generator.generate_voice(test_text, "test_voice.mp3")
    print(f"Voiceover saved to: {path}")
