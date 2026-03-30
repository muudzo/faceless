import httpx
import anyio
from src.utils import setup_logger

logger = setup_logger()

class BaseAPIClient:
    """
    A foundational asynchronous HTTP client providing session management 
    with non-blocking I/O for scalable performance.
    """
    def __init__(self, base_url="", headers=None, timeout=30.0):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            follow_redirects=True
        )

    async def get(self, endpoint="", params=None, **kwargs):
        """
        Executes an asynchronous GET request.
        """
        try:
            response = await self.client.get(endpoint, params=params, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Error {e.response.status_code} at {e.request.url}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Network error at {e.request.url}: {e}")
            raise

    async def close(self):
        """Closes the underlying async client."""
        await self.client.aclose()
