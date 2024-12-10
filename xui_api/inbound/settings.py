from typing import List
from xui_api.client.client_model import Client
from xui_api.inbound.model import JsonModel
from pydantic import Field


class Settings(JsonModel):
    """
    Represents the settings for an inbound connection in the XUI API.

    Attributes:
        clients (list[Client]): A list of clients associated with the inbound connection. Default is an empty list.
        decryption (str): The decryption method used for the inbound connection. Default is "none".
        fallbacks (list): A list of fallback configurations for the inbound connection. Default is an empty list.
    """

    clients: List[Client] = Field(default=[], alias="clients")
    decryption: str = "none"
    fallbacks: List = Field(default=[], alias="fallbacks")
