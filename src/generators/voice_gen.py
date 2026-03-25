from gtts import gTTS
import os
from src.config import PROCESSED_DATA_DIR, VOICE_LANGUAGE, VOICE_SLOW

class VoiceGenerator:
    def __init__(self, lang=VOICE_LANGUAGE, slow=VOICE_SLOW):
        self.lang = lang
        self.slow = slow

    def generate_voice(self, text, filename="voiceover.mp3", speed_up=1.1):
        """
        Generates an MP3 file from text using gTTS and optionally speeds it up.
        """
        tts = gTTS(text=text, lang=self.lang, slow=self.slow)
        temp_path = PROCESSED_DATA_DIR / f"temp_{filename}"
        final_path = PROCESSED_DATA_DIR / filename
        
        tts.save(str(temp_path))
        
        if speed_up != 1.0:
            from moviepy.editor import AudioFileClip
            audio = AudioFileClip(str(temp_path))
            
            # Basic validation: ensure narration isn't empty
            if audio.duration == 0:
                raise ValueError("Generated audio is empty.")
                
            from moviepy.audio.fx.all import speedx, volumex
            # Speed up and normalize volume to -3dB approx (volumex is relative)
            new_audio = speedx(audio, factor=speed_up)
            # Ensure consistent volume levels
            new_audio = volumex(new_audio, factor=1.2) 
            
            new_audio.write_audiofile(str(final_path), verbose=False, logger=None)
            audio.close()
            new_audio.close()
            os.remove(str(temp_path))
        else:
            os.rename(str(temp_path), str(final_path))
            
        return str(final_path)

if __name__ == "__main__":
    generator = VoiceGenerator()
    test_text = "This is a test of the cosmic curiosities voiceover system. Checking one, two, three."
    path = generator.generate_voice(test_text, "test_voice.mp3")
    print(f"Voiceover saved to: {path}")
