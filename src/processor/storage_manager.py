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
        self.temp_dir = self.processed_dir / "temp"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def get_session_dir(self, session_id):
        """Creates and returns a subfolder for a specific production session."""
        session_path = self.temp_dir / f"session_{session_id}"
        session_path.mkdir(parents=True, exist_ok=True)
        return session_path

    def cleanup(self, keep_logs=True, session_id=None):
        """
        Cleans up temporary files, optionally preserving logs and specific sessions.
        """
        target = self.temp_dir if not session_id else (self.temp_dir / f"session_{session_id}")
        if not target.exists():
            return
            
        logger.info(f"Cleaning storage: {target}")
        for path in target.glob("**/*"):
            if path.is_file():
                if keep_logs and path.suffix in [".log", ".db"]:
                    continue
                try:
                    path.unlink()
                except Exception as e:
                    logger.warning(f"Could not delete {path}: {e}")
        
        # Remove empty session dirs
        if session_id:
            try:
                target.rmdir()
            except:
                pass
        

if __name__ == "__main__":
    manager = StorageManager()
    print("StorageManager initialized.")
