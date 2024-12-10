from xui_api.async_3xapi.api_info import InfoApi


class DatabaseApi(InfoApi):
    """
    Provides methods for managing database operations within the XUI API,
    such as creating backups.
    """

    async def backup_db(self) -> None:
        """
        Creates a backup of the database.

        This method sends a request to initiate a database backup and logs
        the operation's progress and success status.
        """
        path = "panel/api/inbounds/createbackup"
        headers = {"Accept": "application/json"}
        url = self._url(path)

        self.logger.info("Initiating database backup...")

        try:
            await self._get_request(url, headers)
            self.logger.info("Database backup completed successfully.")
        except Exception as e:
            self.logger.error(f"Failed to create database backup: {e}")
            raise
