import asyncio
import pytest
import aiohttp
from aioresponses import aioresponses
from unittest.mock import MagicMock
from xui_api.utils.null_logger import NullLogger
from xui_api.async_3xapi.api_info import InfoApi


# Fixture to initialize an instance of InfoApi
@pytest.fixture
def api_instance():
    """Fixture to initialize an instance of InfoApi."""
    return InfoApi(
        host="http://example.com",
        username="test_user",
        password="test_password",
        logger=NullLogger(__name__),
    )


# Tests for the InfoApi class
@pytest.mark.asyncio
async def test_initialization(api_instance):
    """Tests the correct initialization of the InfoApi instance."""
    api = api_instance
    assert api.host == "http://example.com"
    assert api.username == "test_user"
    assert api.password == "test_password"
    assert api.cookie_session is None
    assert api.retry_attempts == 3


@pytest.mark.asyncio
async def test_login_success(api_instance):
    """Tests a successful login."""
    api = api_instance
    with aioresponses() as mock:
        mock.post(
            "http://example.com/login",
            status=200,
            headers={"Set-Cookie": "session=12345"},
        )
        await api.login()
        assert api.cookie_session == {"session": "12345"}


@pytest.mark.asyncio
async def test_login_failure(api_instance):
    """Tests the scenario where login fails."""
    api = api_instance
    with aioresponses() as mock:
        mock.post(
            "http://example.com/login",
            status=401,
            body="Unauthorized",
        )
        with pytest.raises(RuntimeError, match="Login failed. Status code: 401, Response: Unauthorized"):
            await api.login()


@pytest.mark.asyncio
async def test_request_get_success(api_instance):
    """Tests a successful GET request to the API."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    with aioresponses() as mock:
        mock.get(
            "http://example.com/api/test-endpoint",
            status=200,
            payload={"key": "value"},
        )
        response = await api._get_request("http://example.com/api/test-endpoint")
        assert response == {"key": "value"}


@pytest.mark.asyncio
async def test_request_retry(api_instance):
    """Tests the request retry mechanism in case of an error."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    with aioresponses() as mock:
        mock.get(
            "http://example.com/test-endpoint",
            status=500,
            repeat=True,
        )
        url = api._url("test-endpoint")
        with pytest.raises(RuntimeError, match=r"Request failed\. Status code: 500"):
            await api._get_request(url)


@pytest.mark.asyncio
async def test_request_reauth_on_401(api_instance):
    """Tests reauthentication on session expiration (401 Unauthorized)."""
    api = api_instance
    with aioresponses() as mock:
        mock.get("http://example.com/test", status=401)
        mock.get("http://example.com/test", status=200, payload={"message": "Success"})
        mock.post("http://example.com/login", status=200, headers={"Set-Cookie": "session=12345"})
        api.cookie_session = {"session": "expired"}
        result = await api._request("GET", "http://example.com/test")
        assert result == {"message": "Success"}


@pytest.mark.asyncio
async def test_request_without_login(api_instance):
    """Tests that a request without login raises an error."""
    api = api_instance
    with pytest.raises(RuntimeError, match="You must log in before making requests."):
        await api._request("GET", "http://example.com/test")


def test_url_method(api_instance):
    """Tests the _url method for correct URL construction."""
    api = api_instance
    assert api._url("test") == "http://example.com/test"


def test_cookie_session(api_instance):
    """Tests correct saving and retrieval of cookies."""
    api = api_instance
    assert api.cookie_session is None
    api.cookie_session = {"session": "12345"}
    assert api.cookie_session == {"session": "12345"}


@pytest.mark.asyncio
async def test_logging_on_error(api_instance):
    """Tests logger calls when an error occurs."""
    mock_logger = MagicMock()
    api = api_instance
    api.logger = mock_logger
    with aioresponses() as mock:
        mock.post("http://example.com/login", status=401, body="Unauthorized")
        with pytest.raises(RuntimeError):
            await api.login()
    mock_logger.error.assert_called_with("Login failed. Status code: 401, Response: Unauthorized")


@pytest.mark.asyncio
async def test_request_with_custom_headers(api_instance):
    """Tests handling custom headers in the request."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    custom_headers = {"X-Custom-Header": "CustomValue"}
    with aioresponses() as mock:
        mock.get(
            "http://example.com/test-endpoint",
            status=200,
            payload={"key": "value"},
            headers=custom_headers,
        )
        response = await api._get_request("http://example.com/test-endpoint", headers=custom_headers)
        assert response == {"key": "value"}


@pytest.mark.asyncio
async def test_post_request_success(api_instance):
    """Tests a successful POST request to the API."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    payload = {"field": "value"}
    with aioresponses() as mock:
        mock.post(
            "http://example.com/api/test-endpoint",
            status=200,
            payload={"result": "success"},
        )
        response = await api._post_request("http://example.com/api/test-endpoint", data=payload)
        assert response == {"result": "success"}


def test_tls_disabled(api_instance):
    """Tests disabling TLS."""
    api = InfoApi(
        host="http://example.com",
        username="test_user",
        password="test_password",
        tls=False,
        logger=NullLogger(__name__),
    )
    assert not api.tls


@pytest.mark.asyncio
async def test_invalid_response_format(api_instance):
    """Tests handling an invalid JSON response."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    with aioresponses() as mock:
        mock.get(
            "http://example.com/api/test-endpoint",
            status=200,
            body="Invalid JSON",
        )
        with pytest.raises(ValueError, match="Invalid response format."):
            await api._get_request("http://example.com/api/test-endpoint")


@pytest.mark.asyncio
async def test_request_timeout(api_instance):
    """Tests handling a request timeout."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    with aioresponses() as mock:
        mock.get(
            "http://example.com/test-endpoint",
            exception=asyncio.TimeoutError,
        )
        with pytest.raises(asyncio.TimeoutError):
            await api._get_request("http://example.com/test-endpoint")


@pytest.mark.asyncio
async def test_login_multiple_failures(api_instance):
    """Tests behavior on multiple failed login attempts."""
    api = api_instance
    with aioresponses() as mock:
        mock.post(
            "http://example.com/login",
            status=401,
            body="Unauthorized",
        )
        with pytest.raises(RuntimeError, match="Login failed."):
            await api.login()


@pytest.mark.asyncio
async def test_connection_error(api_instance):
    """Tests handling a connection error."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    with pytest.raises(aiohttp.ClientConnectionError):
        await api._get_request("http://nonexistent.example.com/test-endpoint")


@pytest.mark.asyncio
async def test_large_response(api_instance):
    """Tests handling a large response."""
    api = api_instance
    api.cookie_session = {"session": "12345"}
    large_payload = {"data": ["value"] * 1000}
    with aioresponses() as mock:
        mock.get(
            "http://example.com/api/large-endpoint",
            status=200,
            payload=large_payload,
        )
        response = await api._get_request("http://example.com/api/large-endpoint")
        assert response == large_payload
