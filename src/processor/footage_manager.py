import re
from src.apis.pexels_client import PexelsClient
from src.utils import setup_logger

logger = setup_logger()

class FootageManager:
    """
    Manages b-roll footage selection based on script content.
    """
    def __init__(self):
        self.pexels = PexelsClient()

    def extract_keywords(self, script, top_n=3):
        """
        Simple keyword extraction (can be improved with NLP).
        """
        # Remove common stop words and punctuation
        words = re.findall(r'\w+', script.lower())
        stopwords = {'the', 'a', 'is', 'and', 'in', 'of', 'to', 'for', 'with', 'on', 'this', 'you', 'your'}
        candidates = [w for w in words if w not in stopwords and len(w) > 3]
        
        # Count frequencies
        freq = {}
        for w in candidates:
            freq[w] = freq.get(w, 0) + 1
            
        sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [k for k, v in sorted_keywords[:top_n]]

    def get_relevant_footage(self, script):
        """
        Searches Pexels for videos related to the script's theme.
        """
        keywords = self.extract_keywords(script)
        query = " ".join(keywords)
        logger.info(f"Searching footage for: {query}")
        
        try:
            results = self.pexels.search_videos(query, per_page=3)
            videos = results.get("videos", [])
            if not videos:
                # Fallback to general space query
                results = self.pexels.search_videos("outer space", per_page=3)
                videos = results.get("videos", [])
                
            return videos
        except Exception as e:
            logger.error(f"Footage search failed: {e}")
            return []
