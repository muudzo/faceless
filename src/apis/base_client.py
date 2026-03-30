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

    async def get(self, endpoint="", params=None, retries=3, **kwargs):
        """
        Executes an asynchronous GET request with exponential backoff and jitter.
        """
        import random
        import anyio
        
        last_exception = None
        for attempt in range(retries):
            try:
                response = await self.client.get(endpoint, params=params, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                last_exception = e
                if attempt < retries - 1:
                    # Exponential backoff: 1, 2, 4... + jitter
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Retry {attempt + 1}/{retries} in {delay:.2f}s due to: {e}")
                    await anyio.sleep(delay)
                else:
                    logger.error(f"Final failure after {retries} attempts: {e}")
                    raise last_exception

    async def close(self):
        """Closes the underlying async client."""
        await self.client.aclose()
