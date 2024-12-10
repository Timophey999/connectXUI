"""
This module contains the Sniffing class for representing and parsing sniffing settings in the XUI API.
"""

from pydantic import Field
from xui_api.inbound.model import JsonModel


class Sniffing(JsonModel):
    """
    Represents the sniffing settings for an inbound connection in the XUI API.

    Attributes:
        enabled (bool): Whether sniffing is enabled. Default is False.
        dest_override (list[str]): A list of destination overrides. Default is an empty list.
        metadata_only (bool): Whether to only sniff metadata. Default is False.
        route_only (bool): Whether to only sniff routes. Default is False.
    """

    enabled: bool = False
    dest_override: list[str] = Field(default=[], alias="destOverride")
    metadata_only: bool = Field(default=False, alias="metadataOnly")
    route_only: bool = Field(default=False, alias="routeOnly")
