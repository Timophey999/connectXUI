"""
This module defines the StreamSettings class for parsing and representing stream settings in the XUI API.
"""

from typing import Dict, List, Any
from pydantic import Field
from xui_api.inbound.model import JsonModel


class StreamSettings(JsonModel):
    """
    Represents the stream settings for an inbound connection in the XUI API.

    Attributes:
        security (str): The security method for the inbound connection. Default is "none".
        network (str): The network type for the inbound connection. Default is "tcp".
        tcp_settings (dict): The TCP settings for the inbound connection.
        external_proxy (list): A list of external proxies for the inbound connection. Default is an empty list.
        reality_settings (dict): The reality settings for the inbound connection. Default is an empty dictionary.
        xtls_settings (dict): The xTLS settings for the inbound connection. Default is an empty dictionary.
        tls_settings (dict): The TLS settings for the inbound connection. Default is an empty dictionary.
    """

    security: str = "none"
    network: str = "tcp"
    tcp_settings: Dict = Field(
        default={
            "acceptProxyProtocol": False,
            "header": {"type": "none"},
        },
        alias="tcpSettings"
    )
    external_proxy: List = Field(default=[], alias="externalProxy")
    reality_settings: Dict = Field(default={}, alias="realitySettings")
    xtls_settings: Dict = Field(default={}, alias="xtlsSettings")
    tls_settings: Dict = Field(default={}, alias="tlsSettings")
