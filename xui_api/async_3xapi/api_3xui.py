
from xui_api.async_3xapi.api_client import ClientApi
from xui_api.async_3xapi.api_inbound import InboundApi
from xui_api.async_3xapi.api_database import DatabaseApi
from xui_api.utils.null_logger import NullLogger
from typing import Any, Optional


class Async3xui:
    """A unified interface to interact with the Client, Inbound, and Database APIs.
    A unified interface to interact with the Client and Inbound APIs.

    This class handles session management and provides a single entry point
    for API interactions. It supports optional logging and TLS configuration.

    Args:
        host (str): API host URL.
        username (str): Username for authentication.
        password (str): Password for authentication.
        cookie_token (Optional[str]): Optional session token for authentication.
        tls (bool): Whether to use TLS for secure communication. Defaults to True.
        logger (Optional[Any]): Logger instance, defaults to a null logger.

    Attributes:
        client (ClientApi): Interface for client-related API operations.
        inbound (InboundApi): Interface for inbound-related API operations.
        database (DatabaseApi): Interface for database-related API operations.
        _session (Optional[str]): Session token for API interactions.

    Methods:
        login: Authenticates and initializes the session for both APIs.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        cookie_token: Optional[str] = None,
        tls: bool = True,
        logger: Optional[Any] = None,
    ):
        self.logger = logger or NullLogger(__name__)

        self.client = ClientApi(
            host=host,
            username=username,
            password=password,
            cookie_token=cookie_token,
            tls=tls,
        )

        self.inbound = InboundApi(
            host=host,
            username=username,
            password=password,
            cookie_token=cookie_token,
            tls=tls,
        )
        self.database = DatabaseApi(
            host=host,
            username=username,
            password=password,
            cookie_token=cookie_token,
            tls=tls,
        )

        self._session: Optional[str] = None

    @property
    def session(self) -> Optional[str]:
        """Get the current session token."""
        return self._session

    @session.setter
    def session(self, value: Optional[str]) -> None:
        """Set the session token and update it for all API interfaces."""
        self._session = value
        self.client._session = value
        self.inbound._session = value
        self.database._session = value

    async def login(self) -> None:
        """
        Authenticates with the API and sets up the session token.

        This method logs in both the client, inbound, and database interfaces,
        synchronizing the session token for consistent API interactions.

        Raises:
            Exception: If authentication fails.
        """
        await self.client.login()
        self.session = self.client.cookie_session
        self.inbound._session = self._session
        self.database._session = self.session
        self.logger.info("Logged in successfully.")
