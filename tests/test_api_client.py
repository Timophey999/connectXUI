import pytest
from unittest.mock import AsyncMock, MagicMock
from xui_api.client.client_model import Client
from xui_api.async_3xapi.api_client import ClientApi


@pytest.fixture
def client_api_instance():
    """Fixture for initializing a ClientApi instance."""
    client_api = ClientApi(
        host="http://example.com",
        username="test_user",
        password="test_password",
        logger=MagicMock(),
    )
    client_api._get_request = AsyncMock()
    client_api._post_request = AsyncMock()
    return client_api


@pytest.mark.asyncio
async def test_add_client_success(client_api_instance):
    """Test successful addition of a client."""
    client_api = client_api_instance
    mock_client = Client(uuid="123", inbound_id=1, email="test@example.com")
    client_api._post_request.return_value = {"msg": "Client added successfully"}

    await client_api.add_client(1, mock_client)

    client_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/addClient",
        {"Accept": "application/json"},
        {
            "id": 1,
            "settings": '{"clients": [{"email": "test@example.com", "enable": true, "id": "123", "inboundId": 1, "up": 0, '
                        '"down": 0, "expiryTime": 0, "total": 0, "reset": 0, "flow": "", "limitIp": 0, "subId": "", "tgId": "", '
                        '"totalGB": 0}]}',
        },
    )
    client_api.logger.info.assert_called_with("Client added successfully")


@pytest.mark.asyncio
async def test_get_all_clients_success(client_api_instance):
    """Test successful retrieval of all clients."""
    client_api = client_api_instance
    client_api._get_request.return_value = {
        "obj": {"settings": '{"clients": [{"email": "test@example.com"}]}'},
        "msg": "Clients fetched successfully",
    }

    result = await client_api.get_all_clients(1)

    client_api._get_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/get/1",
        {"Accept": "application/json"},
    )
    client_api.logger.info.assert_called_with(f"Retrieved clients for inbound 1")
    assert result == [{"email": "test@example.com"}]


@pytest.mark.asyncio
async def test_update_client_success(client_api_instance):
    """Test successful client update."""
    client_api = client_api_instance
    mock_client = Client(inbound_id=1, email="test@example.com", uuid="1123")
    client_api._post_request.return_value = {"msg": "Client updated successfully"}

    await client_api.update_client("1123", mock_client)

    client_api._post_request.assert_awaited_once_with(
        f"http://example.com/panel/api/inbounds/updateClient/{mock_client.uuid}",
        {"Accept": "application/json"},
        {
            "id": 1,
            "settings": '{"clients": [{"email": "test@example.com", "enable": true, "id": "1123", "inboundId": 1, "up": 0, '
                        '"down": 0, "expiryTime": 0, "total": 0, "reset": 0, "flow": "", "limitIp": 0, "subId": "", "tgId": "", '
                        '"totalGB": 0}]}',
        },
    )
    client_api.logger.info.assert_called_with("Updated client 1123")


@pytest.mark.asyncio
async def test_get_by_email_success(client_api_instance):
    """Test successful client retrieval by email."""
    client_api = client_api_instance
    client_api._get_request.return_value = {"obj": {"inboundId": 1}}
    client_api.get_all_clients = AsyncMock(
        return_value=[{"email": "test@example.com", "id": "1123", "inboundId": 1}]
    )

    result = await client_api.get_by_email("test@example.com")

    client_api._get_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/getClientTraffics/test@example.com",
        {"Accept": "application/json"},
    )
    client_api.get_all_clients.assert_awaited_once_with(1)
    client_api.logger.info.assert_called_with(
        "Fetched client by email: test@example.com"
    )
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_delete_client_success(client_api_instance):
    """Test successful client deletion."""
    client_api = client_api_instance
    client_api.get_all_clients = AsyncMock(
        return_value=[{"email": "test@example.com", "id": "uuid-1234"}]
    )
    client_api._post_request.return_value = {"msg": "Client deleted successfully"}

    await client_api.delete_client(1, "test@example.com")

    client_api.get_all_clients.assert_awaited_once_with(1)
    client_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/1/delClient/uuid-1234",
        {"Accept": "application/json"},
    )
    client_api.logger.info.assert_called_with(
        "Deleted client test@example.com"
    )


@pytest.mark.asyncio
async def test_get_client_not_found(client_api_instance):
    """Test error handling for a non-existent client."""
    client_api = client_api_instance
    client_api._get_request.side_effect = Exception("404 Client Not Found")

    with pytest.raises(Exception, match="404 Client Not Found"):
        await client_api.get_all_clients(999)


@pytest.mark.asyncio
async def test_server_error(client_api_instance):
    """Test error handling for a server error."""
    client_api = client_api_instance
    client_api._post_request.side_effect = Exception("500 Internal Server Error")
    client = Client(email="test@example.com", uuid="1234", inbound_id=1)

    with pytest.raises(Exception, match="500 Internal Server Error"):
        await client_api.add_client(1, client)


@pytest.mark.asyncio
async def test_add_client_large_data(client_api_instance):
    """Test handling of a client with large data."""
    client_api = client_api_instance
    large_email = "a" * 500 + "@example.com"
    mock_client = Client(uuid="123", inbound_id=1, email=large_email)
    client_api._post_request.return_value = {"msg": "Client added successfully"}

    await client_api.add_client(1, mock_client)

    client_api.logger.info.assert_called_with("Client added successfully")
