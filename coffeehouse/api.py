from .exception import CoffeeHouseError

import aiohttp
import asyncio


__all__ = ["API"]


class API:
    """Base class for all CoffeeHouse services.
    It can be instantiated by itself as a holder for the API key,
    or it can be subclassed by CoffeeHouse services.
    
    Parameters:
        access_key (``str``):
            Access key from coffeehouse.intellivoid.info
            
        endpoint (``str``):
            Base URL for all requests, without the trailing slash
            
        loop (`EventLoop <https://docs.python.org/3/library/\
                asyncio-eventloop.html#asyncio-event-loop>_`, optional):
            The event loop to be passed to aiohttp.ClientSession

        session (:obj:`aiohttp.ClientSession`, optional):
            The aiohttp.ClientSession object to be used for HTTP requests
    """

    def __init__(
        self,
        access_key,
        endpoint="https://api.intellivoid.net/coffeehouse",
        loop=None,
        session=None
        ):
        if isinstance(access_key, API):
            self.access_key = access_key.access_key
            self.endpoint = access_key.endpoint
        else:
            self.access_key = access_key
            self.endpoint = endpoint
        if not loop:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop
        if not session:
            self._session = aiohttp.ClientSession(loop=self._loop)
        else:
            self._session = session

    async def _send(self, path, access_key=True, **payload):
        """Send a request to the server configured by self.endpoint.
        
        Parameters:
            path (``str``):
                The path over the base URL, without the preceding slash
                
        Returns:
            response (``dict``):
                The parsed response is returned
        """
        if access_key:
            payload["access_key"] = self.access_key
        async with self._session.post(
            "{}/{}".format(self.endpoint, path),
            data=payload
        ) as res:
            res_status = res.status
            res_text = await res.text()
        request_id = None
        if "x-request-id" in res.headers:
            request_id = res.headers["x-request-id"]
        return CoffeeHouseError.parse_and_raise(
            res_status,
            res_text,
            request_id)["payload"]
            
    async def close(self):
        """Close aiohttp.ClientSession object"""
        await self._session.close()
