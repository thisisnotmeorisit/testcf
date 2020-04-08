from .session import LydiaSession
from ..api import API
from ..exception import CoffeeHouseError


__all__ = ["LydiaAI"]


class LydiaAI(API):
    def __init__(self, *args, **kwargs):
        """
        Public constructor for Lydia
        
        Parameters:
            access_key (``str``):
                Access key from coffeehouse.intellivoid.info
            
            endpoint (``str``):
                Base URL for all requests, without the trailing slash
        """

        super().__init__(*args, **kwargs)

    async def create_session(self, language="en"):
        """
        Create a new LydiaSession with the AI
        
        Parameters:
            language (``str``):
                The language the session should be based in
                
        Returns:
            :obj:`LydiaSession`: On success, the newly created session is returned
            
        Raises:
            CoffeeHouseError
        """

        return LydiaSession(await self._send("v1/lydia/session/create",
                                       target_language=language), self)

    async def get_session(self, session_id):
        """
        Get an existing session using a LydiaSession ID
        
        Parameters:
            session_id (``str``):
                The ID of the session to retrieve
        
        Returns:
            :obj:`LydiaSession`: The specified session is returned
            
        Raises:
            CoffeeHouseError
        """

        return LydiaSession(await self._send("v1/lydia/session/get",
                                       session_id=session_id), self)

    async def think_thought(self, session_id, text):
        """
        Process user input and return an AI text response
        
        Parameters:
            session_id (``str``):
                The unique ID of the session
            
            text (``str``):
                The user input
                
        Returns:
            On success, the response of the AI is returned
            
        Raises:
            CoffeeHouseError
        """

        return (await self._send("v1/lydia/session/think",
                          session_id=session_id,
                          input=text))["output"]
