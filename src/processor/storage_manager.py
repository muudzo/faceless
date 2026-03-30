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
        self.base_temp_dir = self.processed_dir / "sessions"
        self.base_temp_dir.mkdir(parents=True, exist_ok=True)

    def get_session_dir(self, session_id=None):
        """
        Creates and returns a subfolder for a specific production session.
        If no session_id is provided, it uses a timestamp-based ID.
        """
        if not session_id:
            import datetime
            session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
        session_path = self.base_temp_dir / f"session_{session_id}"
        session_path.mkdir(parents=True, exist_ok=True)
        # Set restrictive permissions (700) for security
        os.chmod(session_path, 0o700)
        return session_path

    def cleanup(self, session_id, keep_logs=True):
        """
        Cleans up a specific session directory.
        """
        target = self.base_temp_dir / f"session_{session_id}"
        if not target.exists():
            return
            
        from src.utils import setup_logger
        logger = setup_logger()
        
        logger.info(f"Cleaning session storage: {target}")
        import shutil
        try:
            shutil.rmtree(target)
        except Exception as e:
            logger.warning(f"Could not delete session {session_id}: {e}")
        

if __name__ == "__main__":
    manager = StorageManager()
    print("StorageManager initialized.")
