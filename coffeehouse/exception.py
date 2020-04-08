import json


__all__ = ["CoffeeHouseError"]


class CoffeeHouseError(Exception):
    """
    Exception raised by API errors.
    The exception message is set to the server's response.
    
    Parameters:
        status_code (``int``):
            Status code returned by the server
            
        message (``str``):
            Response content returned by the server
            
        request_id (``str``):
            The request ID returned by the server
    """

    def __init__(self, status_code, content, request_id):
        self.status_code = status_code
        self.content = content
        self.request_id = request_id
        self.message = content.get("message", None) if content else "Unknown"
        super().__init__(self.message or content)

    @staticmethod
    def parse_and_raise(status_code, content, request_id):
        """
        Raise an exception if applicable, otherwise return the
        response of the method
        
        Parameters:
            status_code (``int``):
                Status code returned by the server
            
            content (``str``):
                Response content returned by the server
                
            request_id (``str``):
                The request ID returned by the server
                
        Returns:
            response (``dict``):
                The response returned by the server
            
        Raises:
            CoffeeHouseError
        """

        try:
            response = json.loads(content)
        except json.decoder.JSONDecodeError:
            raise CoffeeHouseError(status_code, None, request_id)
        if status_code != 200:
            raise _mapping.get(status_code,
                               CoffeeHouseError)(status_code, response, request_id)
        return response


class ApiSuspendedError(CoffeeHouseError):
    pass


class InvalidApiKeyError(CoffeeHouseError):
    pass


class AIError(CoffeeHouseError):
    pass


class SessionInvalidError(CoffeeHouseError):
    pass


class SessionNotFoundError(CoffeeHouseError):
    pass


_mapping = {
    400: SessionInvalidError,
    401: InvalidApiKeyError,
    403: ApiSuspendedError,
    404: SessionNotFoundError,
    503: AIError
}