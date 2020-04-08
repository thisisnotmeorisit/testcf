__all__ = ["LydiaSession", "Session"]


class LydiaSession:
    def __init__(self, data, client):
        """
        AI Session Object
        """

        self._client = client
        self.id = data["session_id"]
        self.language = data["language"]
        self.available = data["available"]
        self.expires = data["expires"]

    async def think_thought(self, text):
        """
        Processes user input and returns an AI text Response

        Parameters:
            text (``str``):
                The user input
            
        Returns:
            response (``str``):
                On success, the response of the AI is returned

        Raises:
            CoffeeHouseError
        """

        return await self._client.think_thought(self.id, text)
        
    async def close(self):
        await self._client.close()

    def __str__(self):
        """
        Return an identifier uniquely specifying this session

        Returns:
            Session ID (``str``)
        """

        return self.id


Session = LydiaSession  # For compatibility
