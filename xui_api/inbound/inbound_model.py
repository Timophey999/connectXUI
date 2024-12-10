"""
This module defines the `Inbound` class, which represents an inbound connection
for the XUI API. It includes configuration settings, stream settings, and more.
"""

from typing import Any, List
from random import randint
from pydantic import BaseModel, ConfigDict, Field

from xui_api.client.client_model import Client
from xui_api.inbound.settings import Settings
from xui_api.inbound.sniffing import Sniffing
from xui_api.inbound.stream_settings import StreamSettings

class Inbound(BaseModel):
    """
    Represents an inbound connection in the XUI API.

    Attributes:
        enable (bool): Whether the inbound connection is enabled.
        port (int): Port number for the inbound connection.
        protocol (str): Protocol for the inbound connection.
        settings (Settings): Connection-specific settings.
        stream_settings (StreamSettings): Stream settings for the connection.
        sniffing (Sniffing): Sniffing settings for the connection.
        listen (str): Optional listen address.
        remark (str): Optional remark for the connection.
        inbound_id (int): Optional unique ID for the connection.
        up (int): Optional uplink data usage in bytes.
        down (int): Optional downlink data usage in bytes.
        total (int): Optional total data usage limit in bytes.
        expiry_time (int): Optional expiry time in UNIX timestamp.
        client_stats (List[Client]): Optional client statistics.
        tag (str): Optional tag for the connection.
    """

    enable: bool = True
    port: int = randint(10000, 99999)
    protocol: str = "vless"
    settings: Settings = Field(default_factory=Settings)
    stream_settings: StreamSettings = Field(default_factory=StreamSettings, alias="streamSettings")
    sniffing: Sniffing = Field(default_factory=Sniffing)

    listen: str = ""
    remark: str = ""
    inbound_id: int = Field(default=0, alias="id")

    up: int = 0
    down: int = 0
    total: int = 0

    expiry_time: int = Field(default=0, alias="expiryTime")
    client_stats: List[Client] = Field(default=list, alias="clientStats")
    tag: str = ""

    model_config = ConfigDict(populate_by_name=True)

    def to_json(self) -> dict[str, Any]:
        """
        Converts the `Inbound` instance into a JSON-compatible dictionary for the XUI API.

        Returns:
            dict[str, Any]: JSON-compatible dictionary representation.
        """
        included_fields = {
            "remark",
            "enable",
            "listen",
            "port",
            "protocol",
            "expiryTime",
        }

        # Include only the necessary fields and alias others for API compatibility.
        base_data = super().model_dump(by_alias=True)
        filtered_data = {key: value for key, value in base_data.items() if key in included_fields}

        # Add nested object representations.
        filtered_data.update({
            "settings": self.settings.model_dump_json(by_alias=True),
            "streamSettings": self.stream_settings.model_dump_json(by_alias=True),
            "sniffing": self.sniffing.model_dump_json(by_alias=True),
        })

        return filtered_data
