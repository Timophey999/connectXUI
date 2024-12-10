"""
Unit tests for the InboundApi class, testing various operations related to inbound connections.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from xui_api.inbound.inbound_model import Inbound
from xui_api.async_3xapi.api_inbound import InboundApi


@pytest.fixture
def inbound_api_instance():
    """Fixture to initialize an InboundApi instance."""
    api_instance = InboundApi(
        host="http://example.com",
        username="test_user",
        password="test_password",
        logger=MagicMock(),
    )
    api_instance._get_request = AsyncMock()
    api_instance._post_request = AsyncMock()
    return api_instance


@pytest.mark.asyncio
async def test_get_list_success(inbound_api_instance):
    """Test successful retrieval of the inbound list."""
    inbound_api = inbound_api_instance
    mock_response = {
        "obj": [{"id": 1, "settings": '{"clients": []}'}],
        "msg": "List fetched successfully",
    }
    inbound_api._get_request.return_value = mock_response

    result = await inbound_api.get_list()

    inbound_api._get_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/list", {"Accept": "application/json"}
    )
    inbound_api.logger.info.assert_called_with("List fetched successfully")
    assert len(result) == 1
    assert isinstance(result[0], Inbound)


@pytest.mark.asyncio
async def test_add_success(inbound_api_instance):
    """Test successful addition of a new inbound."""
    inbound_api = inbound_api_instance
    mock_inbound = Inbound(inbound_id=1, settings='{"clients": []}')
    inbound_api._post_request.return_value = {"msg": "Inbound added successfully"}

    await inbound_api.add(mock_inbound)

    inbound_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/add",
        {"Accept": "application/json"},
        mock_inbound.to_json(),
    )
    inbound_api.logger.info.assert_called_with("Inbound added successfully")


@pytest.mark.asyncio
async def test_get_by_id_success(inbound_api_instance):
    """Test successful retrieval of an inbound by ID."""
    inbound_api = inbound_api_instance
    mock_response = {"obj": {"id": 1, "settings": '{"clients": []}'}, "msg": "Success"}

    inbound_api._get_request.return_value = mock_response

    result = await inbound_api.get_by_id(inbound_id=1)

    inbound_api._get_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/get/1", {"Accept": "application/json"}
    )
    inbound_api.logger.info.assert_called_with("Success")

    assert isinstance(result, Inbound)
    assert result.inbound_id == 1


@pytest.mark.asyncio
async def test_delete_success(inbound_api_instance):
    """Test successful deletion of an inbound by ID."""
    inbound_api = inbound_api_instance
    inbound_api._post_request.return_value = {"msg": "Inbound deleted successfully"}

    await inbound_api.delete(1)

    inbound_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/del/1", {"Accept": "application/json"}
    )
    inbound_api.logger.info.assert_called_with("Inbound deleted successfully")


@pytest.mark.asyncio
async def test_update_success(inbound_api_instance):
    """Test successful update of an inbound."""
    inbound_api = inbound_api_instance
    mock_inbound = Inbound(inbound_id=1, settings='{"clients": []}')
    inbound_api._post_request.return_value = {"msg": "Inbound updated successfully"}

    await inbound_api.update(1, mock_inbound)

    inbound_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/update/1",
        {"Accept": "application/json"},
        mock_inbound.to_json(),
    )
    inbound_api.logger.info.assert_called_with("Inbound updated successfully")


@pytest.mark.asyncio
async def test_reset_all_stats_success(inbound_api_instance):
    """Test successful reset of all inbound traffic statistics."""
    inbound_api = inbound_api_instance
    inbound_api._post_request.return_value = {"msg": "All traffic stats reset"}

    await inbound_api.reset_all_stats()

    inbound_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/resetAllTraffics", {"Accept": "application/json"}
    )
    inbound_api.logger.info.assert_called_with("All traffic stats reset")


@pytest.mark.asyncio
async def test_reset_inbound_stats_success(inbound_api_instance):
    """Test successful reset of traffic statistics for a specific inbound."""
    inbound_api = inbound_api_instance
    inbound_api._post_request.return_value = {"msg": "Inbound stats reset"}

    await inbound_api.reset_inbound_stats(1)

    inbound_api._post_request.assert_awaited_once_with(
        "http://example.com/panel/api/inbounds/resetAllClientTraffics/1",
        {"Accept": "application/json"},
    )
    inbound_api.logger.info.assert_called_with("Inbound stats reset")
