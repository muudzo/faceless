import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from src.utils import setup_logger

logger = setup_logger()

class BaseAPIClient:
    """
    A foundational HTTP client providing session management with automatic
    retries for robust external API communication.
    """
    def __init__(self, base_url="", headers=None, retries=3, backoff_factor=1.0, status_forcelist=(500, 502, 503, 504)):
        self.base_url = base_url
        self.session = requests.Session()
        
        if headers:
            self.session.headers.update(headers)
            
        retry_strategy = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def get(self, endpoint="", params=None, stream=False, **kwargs):
        """
        Executes a GET request against the configured base_url.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, stream=stream, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP GET Request failed to {url}: {e}")
            raise

    def close(self):
        self.session.close()
