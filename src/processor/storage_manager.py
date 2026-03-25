import os
from pathlib import Path
from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

class StorageManager:
    """
    Manages project storage and cleans up temporary files.
    """
    def __init__(self, raw_dir=RAW_DATA_DIR, processed_dir=PROCESSED_DATA_DIR):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir

    def cleanup_temp_files(self, keep_vids=False):
        """
        Removes temporary assets like voiceovers and NASA images.
        """
        extensions_to_remove = [".mp3", ".jpg", ".png"]
        if not keep_vids:
            extensions_to_remove.append(".mp4")
            
        count = 0
        for directory in [self.raw_dir, self.processed_dir]:
            for file in directory.iterdir():
                if file.suffix.lower() in extensions_to_remove and not file.name.startswith("."):
                    try:
                        os.remove(file)
                        count += 1
                    except Exception as e:
                        print(f"Failed to remove {file}: {e}")
        
        return count

if __name__ == "__main__":
    manager = StorageManager()
    print("StorageManager initialized.")
