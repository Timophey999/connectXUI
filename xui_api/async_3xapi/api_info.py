import aiohttp
from typing import Any, Optional, Dict
import json
from xui_api.utils.null_logger import NullLogger


class InfoApi:
    """
    A class for interacting with the XUI API, providing methods for authentication
    and making HTTP requests.
    """

    def __init__(
            self,
            host: str,
            username: str,
            password: str,
            cookie_token: Optional[Dict[str, str]] = None,
            tls: bool = True,
            logger: Optional[Any] = None,
            retry_attempts: int = 3,
    ):
        """
        Initializes the API instance.

        :param host: Base API URL.
        :param username: Username for authentication.
        :param password: Password for authentication.
        :param cookie_token: Optional session cookie.
        :param tls: Whether to use HTTPS (default: True).
        :param logger: Logger instance (default: NullLogger).
        :param retry_attempts: Number of retry attempts for requests.
        """
        self._host = host.rstrip("/")
        self._username = username
        self._password = password
        self._tls = tls
        self._cookie_session = cookie_token
        self.logger = logger or NullLogger(__name__)
        self.retry_attempts = retry_attempts

    @property
    def host(self) -> str:
        """Returns the base API URL."""
        return self._host

    @property
    def username(self) -> str:
        """Returns the username."""
        return self._username

    @property
    def password(self) -> str:
        """Returns the password."""
        return self._password

    @property
    def tls(self) -> bool:
        """Returns the TLS state."""
        return self._tls

    @property
    def cookie_session(self) -> Optional[Dict[str, str]]:
        """Returns the current session as a dictionary."""
        return self._cookie_session

    @cookie_session.setter
    def cookie_session(self, value: Optional[Dict[str, str]]) -> None:
        """Sets the current session cookie."""
        self._cookie_session = value

    def _url(self, path: str) -> str:
        """
        Constructs the full URL for a given API endpoint.

        :param path: Endpoint path.
        :return: Full URL.
        """
        return f"{self._host}/{path}"

    async def login(self) -> None:
        """
        Authenticates with the API and stores the session cookie.
        Raises RuntimeError on failure.
        """
        url = self._url("login")
        headers = {"Accept": "application/json"}
        login_data = {"username": self.username, "password": self.password}

        self.logger.debug(f"Attempting login at: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=login_data) as response:
                if response.status == 200:
                    if response.cookies:
                        self.cookie_session = {key: morsel.value for key, morsel in response.cookies.items()}
                        self.logger.info("Login successful.")
                    else:
                        self.logger.error("Login failed: no cookies returned.")
                        raise RuntimeError("Authentication failed: no cookies returned.")
                else:
                    error_message = (
                        f"Login failed. Status code: {response.status}, "
                        f"Response: {await response.text()}"
                    )
                    self.logger.error(error_message)
                    raise RuntimeError(error_message)

    async def _request(
            self,
            method: str,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, str]] = None,
            attempts_left: Optional[int] = None,
            **kwargs: Any,
    ) -> Any:
        """
        Sends an HTTP request with the specified method and parameters.
        Retries on failure up to `retry_attempts` times.
        Raises RuntimeError on failure.

        :param method: HTTP method (GET, POST, etc.).
        :param url: Request URL.
        :param headers: Optional headers for the request.
        :param data: Optional data payload.
        :param params: Optional query parameters.
        :param attempts_left: Remaining retry attempts.
        :param kwargs: Additional arguments for aiohttp.
        :return: Parsed JSON response or raises an exception.
        """
        if not self.cookie_session:
            raise RuntimeError("You must log in before making requests.")

        attempts_left = attempts_left if attempts_left is not None else self.retry_attempts
        headers = headers or {}

        self.logger.debug(f"Sending {method} request to: {url} with params: {params}, attempts left: {attempts_left}")

        async with aiohttp.ClientSession(cookies=self.cookie_session) as session:
            async with session.request(
                    method, url, headers=headers, data=data, params=params, **kwargs
            ) as response:
                if response.status == 200:
                    try:
                        json_data = await response.json()
                        self.logger.debug(f"Received response: {json_data}")
                        return json_data
                    except aiohttp.ContentTypeError as e:
                        error_message = f"Invalid response format. Response: {await response.text()}"
                        self.logger.error(error_message)
                        raise ValueError(error_message) from e
                    except json.JSONDecodeError:
                        raise ValueError("Invalid response format.")
                elif response.status == 401 and attempts_left > 0:
                    self.logger.info("Session expired, re-authenticating...")
                    await self.login()
                    return await self._request(
                        method, url, headers, data, params, attempts_left=attempts_left - 1, **kwargs
                    )
                elif attempts_left > 0:
                    self.logger.warning(
                        f"Request failed. Status code: {response.status}, retrying ({self.retry_attempts - attempts_left + 1}/{self.retry_attempts})..."
                    )
                    return await self._request(
                        method, url, headers, data, params, attempts_left=attempts_left - 1, **kwargs
                    )
                else:
                    error_message = (
                        f"Request failed. Status code: {response.status}, "
                        f"Response: {await response.text()}"
                    )
                    self.logger.error(error_message)
                    raise RuntimeError(error_message)

    async def _get_request(
            self,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, str]] = None,
            **kwargs: Any,
    ) -> Any:
        """
        Sends a GET request.

        :param url: Request URL.
        :param headers: Optional headers for the request.
        :param params: Optional query parameters.
        :param kwargs: Additional arguments for aiohttp.
        :return: Parsed JSON response or raises an exception.
        """
        return await self._request("GET", url, headers=headers, params=params, **kwargs)

    async def _post_request(
            self,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, str]] = None,
            **kwargs: Any,
    ) -> Any:
        """
        Sends a POST request.

        :param url: Request URL.
        :param headers: Optional headers for the request.
        :param data: Optional payload for the request.
        :param params: Optional query parameters.
        :param kwargs: Additional arguments for aiohttp.
        :return: Parsed JSON response or raises an exception.
        """
        return await self._request("POST", url, headers=headers, data=data, params=params, **kwargs)
