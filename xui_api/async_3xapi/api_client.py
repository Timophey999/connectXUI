from typing import List, Optional
import json
from xui_api.async_3xapi.api_info import InfoApi
from xui_api.client.client_model import Client


class ClientApi(InfoApi):
    async def add_client(self, inbound_id: int, client: Client) -> None:
        """Adds a new client to the specified inbound."""
        url = self._url("panel/api/inbounds/addClient")
        headers = {"Accept": "application/json"}
        settings = {"clients": [client.to_json()]}
        data = {"id": inbound_id, "settings": json.dumps(settings)}

        try:
            response = await self._post_request(url, headers, data)
            self.logger.info(response["msg"])
        except Exception as e:
            self.logger.error(f"Error adding client to inbound {inbound_id}: {e}", exc_info=True)
            raise

    async def get_all_clients(self, inbound_id: int) -> List[dict]:
        """Retrieves a list of all clients for the given inbound ID."""
        url = self._url(f"panel/api/inbounds/get/{inbound_id}")
        headers = {"Accept": "application/json"}

        try:
            response = await self._get_request(url, headers)
            clients_list = json.loads(response['obj']['settings'])
            self.logger.info(f"Retrieved clients for inbound {inbound_id}")
            return clients_list.get('clients', [])
        except Exception as e:
            self.logger.error(f"Error fetching clients for inbound {inbound_id}: {e}", exc_info=True)
            raise

    async def update_client(self, uuid: str, client: Client) -> None:
        """Updates the client data by UUID."""
        url = self._url(f"panel/api/inbounds/updateClient/{uuid}")
        headers = {"Accept": "application/json"}
        settings = {"clients": [client.to_json()]}
        data = {"id": client.inbound_id, "settings": json.dumps(settings)}

        try:
            response = await self._post_request(url, headers, data)
            self.logger.info(f"Updated client {uuid}")
        except Exception as e:
            self.logger.error(f"Error updating client with UUID {uuid}: {e}", exc_info=True)
            raise

    async def get_by_email(self, email: str) -> Optional[Client]:
        """Retrieves client information by email."""
        url = self._url(f"panel/api/inbounds/getClientTraffics/{email}")
        headers = {"Accept": "application/json"}

        try:
            response = await self._get_request(url, headers)
            client_json = response.get('obj')
            if not client_json:
                self.logger.warning(f"No client found with email: {email}")
                return None

            all_clients = await self.get_all_clients(client_json['inboundId'])
            client_data = {client['email']: client for client in all_clients}.get(email)
            if not client_data:
                self.logger.warning(f"No matching client data found for email: {email}")
                return None

            self.logger.info(f"Fetched client by email: {email}")
            return Client.model_validate(client_data)
        except Exception as e:
            self.logger.error(f"Error fetching client by email {email}: {e}", exc_info=True)
            raise

    async def get_ips(self, email: str) -> List[str]:
        """Retrieves the list of IP addresses associated with the client by email."""
        url = self._url(f"panel/api/inbounds/clientIps/{email}")
        headers = {"Accept": "application/json"}

        try:
            response = await self._post_request(url, headers)
            self.logger.info(f"Fetched IPs for email: {email}")
            return response.get('obj', []) if response.get('obj') != 'No IP Record' else []
        except Exception as e:
            self.logger.error(f"Error fetching IPs for email {email}: {e}", exc_info=True)
            raise

    async def reset_stats(self, inbound_id: int, email: str) -> None:
        """Resets traffic statistics for the client by email."""
        url = self._url(f"panel/api/inbounds/{inbound_id}/resetClientTraffic/{email}")
        headers = {"Accept": "application/json"}

        try:
            response = await self._post_request(url, headers)
            self.logger.info(f"Reset stats for email: {email}")
        except Exception as e:
            self.logger.error(f"Error resetting stats for email {email}: {e}", exc_info=True)
            raise

    async def delete_client(self, inbound_id: int, email: str) -> None:
        """Deletes a client by email."""
        try:
            all_clients = await self.get_all_clients(inbound_id)
            client_data = {client['email']: client for client in all_clients}.get(email)
            if not client_data:
                self.logger.warning(f"No client found with email: {email}")
                return

            client_uuid = client_data['id']
            url = self._url(f"panel/api/inbounds/{inbound_id}/delClient/{client_uuid}")
            headers = {"Accept": "application/json"}

            response = await self._post_request(url, headers)
            self.logger.info(f"Deleted client {email}")
        except Exception as e:
            self.logger.error(f"Error deleting client {email}: {e}", exc_info=True)
            raise

    async def delete_depleted(self, inbound_id: int) -> None:
        """Deletes all clients with depleted traffic for the specified inbound."""
        url = self._url(f"panel/api/inbounds/delDepletedClients/{inbound_id}")
        headers = {"Accept": "application/json"}

        try:
            response = await self._post_request(url, headers)
            self.logger.info(f"Deleted depleted clients for inbound {inbound_id}")
        except Exception as e:
            self.logger.error(f"Error deleting depleted clients for inbound {inbound_id}: {e}", exc_info=True)
            raise

    async def get_online(self) -> List[str]:
        """Returns a list of online clients."""
        url = self._url("panel/api/inbounds/onlines")
        headers = {"Accept": "application/json"}

        try:
            response = await self._post_request(url, headers)
            self.logger.info("Retrieved online clients")
            return response.get('obj', [])
        except Exception as e:
            self.logger.error(f"Error fetching online clients: {e}", exc_info=True)
            raise

    async def get_traffic_by_id(self, inbound_id: int, email: str) -> Client:
        """Retrieves traffic data for the client by email and inbound ID."""
        try:
            all_clients = await self.get_all_clients(inbound_id)
            client_data = {client['email']: client for client in all_clients}.get(email)
            if not client_data:
                raise ValueError(f"No client found with email: {email}")

            client_uuid = client_data['id']
            url = self._url(f"panel/api/inbounds/getClientTrafficsById/{client_uuid}")
            headers = {"Accept": "application/json"}

            response = await self._get_request(url, headers)
            self.logger.info(f"Fetched traffic data for email: {email}")
            return Client.model_validate(response['obj'][0])
        except Exception as e:
            self.logger.error(f"Error fetching traffic data for email {email}: {e}", exc_info=True)
            raise
