import aiohttp
from io import BytesIO
import numpy as np
import cv2 as cv

class aioreq():
    def __init__(self):
        self.session = aiohttp.ClientSession(
                headers=None,
                timeout=aiohttp.ClientTimeout(total=60.0)
        )        

    async def magic(self, url: str, magnitude: float = 0.6) -> BytesIO:
        """Applies a magic filter to a given image. Gif."""

        async with self.session.get(url) as resp:

            data = await resp.read()

        image = np.asarray(bytearray(data), dtype="uint8")
        image = cv.imdecode(image, cv.IMREAD_COLOR)
        return image

    async def close(self) -> None:
        """Closes the Client."""
        return await self.session.close()
