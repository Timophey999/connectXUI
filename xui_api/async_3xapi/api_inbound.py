"""This module provides the InboundApi class for managing inbound connections via the XUI API."""

from xui_api.async_3xapi.api_info import InfoApi
from xui_api.inbound.inbound_model import Inbound


class InboundApi(InfoApi):
    """Handles operations related to inbound connections."""

    async def get_list(self) -> list[Inbound]:
        """Fetches the list of all inbound connections.

        Returns:
            list[Inbound]: A list of Inbound instances.
        """
        path = "panel/api/inbounds/list"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)

        try:
            response = await self._get_request(url, headers)
            self.logger.info(response["msg"])
            return [Inbound.model_validate(obj) for obj in response.get("obj", [])]
        except Exception as e:
            self.logger.error(f"Error fetching inbound list: {e}", exc_info=True)
            raise

    async def add(self, inbound: Inbound) -> None:
        """Adds a new inbound connection.

        Args:
            inbound (Inbound): The Inbound instance to add.
        """
        path = "panel/api/inbounds/add"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)
        data = inbound.to_json()

        try:
            response = await self._post_request(url, headers, data)
            self.logger.info(response["msg"])
        except Exception as e:
            self.logger.error(f"Error adding inbound: {e}", exc_info=True)
            raise

    async def get_by_id(self, inbound_id: int) -> Inbound:
        """Fetches details of a specific inbound connection by its ID.

        Args:
            inbound_id (int): The ID of the inbound connection.

        Returns:
            Inbound: The corresponding Inbound instance.
        """
        path = f"panel/api/inbounds/get/{inbound_id}"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)

        try:
            response = await self._get_request(url, headers)
            self.logger.info(response["msg"])
            return Inbound.model_validate(response.get("obj", {}))
        except Exception as e:
            self.logger.error(f"Error fetching inbound by ID {inbound_id}: {e}", exc_info=True)
            raise

    async def delete(self, inbound_id: int) -> None:
        """Deletes an inbound connection by its ID.

        Args:
            inbound_id (int): The ID of the inbound connection to delete.
        """
        path = f"panel/api/inbounds/del/{inbound_id}"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)

        try:
            response = await self._post_request(url, headers)
            self.logger.info(response["msg"])
        except Exception as e:
            self.logger.error(f"Error deleting inbound ID {inbound_id}: {e}", exc_info=True)
            raise

    async def update(self, inbound_id: int, inbound: Inbound) -> None:
        """Updates an existing inbound connection.

        Args:
            inbound_id (int): The ID of the inbound connection to update.
            inbound (Inbound): The updated Inbound instance.
        """
        path = f"panel/api/inbounds/update/{inbound_id}"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)
        data = inbound.to_json()

        try:
            response = await self._post_request(url, headers, data)
            self.logger.info(response['msg'])
        except Exception as e:
            self.logger.error(f"Error updating inbound ID {inbound_id}: {e}", exc_info=True)
            raise

    async def reset_all_stats(self) -> None:
        """Resets traffic statistics for all inbound connections."""
        path = "panel/api/inbounds/resetAllTraffics"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)

        try:
            response = await self._post_request(url, headers)
            self.logger.info(response['msg'])
        except Exception as e:
            self.logger.error(f"Error resetting all traffic statistics: {e}", exc_info=True)
            raise

    async def reset_inbound_stats(self, inbound_id: int) -> None:
        """Resets traffic statistics for a specific inbound connection.

        Args:
            inbound_id (int): The ID of the inbound connection.
        """
        path = f"panel/api/inbounds/resetAllClientTraffics/{inbound_id}"
        headers = {"Accept": "application/json"}
        url = self._url(path=path)

        try:
            response = await self._post_request(url, headers)
            self.logger.info(response['msg'])
        except Exception as e:
            self.logger.error(f"Error resetting traffic statistics for inbound ID {inbound_id}: {e}", exc_info=True)
            raise
