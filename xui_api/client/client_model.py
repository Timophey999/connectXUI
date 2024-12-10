"""
This module defines the `Client` class, representing a client in the XUI API.
"""

from pydantic import BaseModel, Field, ConfigDict


class Client(BaseModel):
    """
    Represents a client in the XUI API.

    Attributes:
        email (str): Email address of the client.
        enable (bool): Indicates whether the client is enabled.
        uuid (int | str): Unique identifier for the client.
        inbound_id (int | None): ID of the inbound connection associated with the client.
        up (int): Upload speed in bytes.
        down (int): Download speed in bytes.
        expiry_time (int): Expiry time as a UNIX timestamp.
        total (int): Total data usage in bytes.
        reset (int): Last reset time as a UNIX timestamp.
        flow (str): Flow configuration for the client.
        limit_ip (int): Limit on the number of IPs the client can use.
        sub_id (str): Subscription ID for the client.
        tg_id (str): Telegram ID associated with the client.
        total_gb (int): Total data usage in gigabytes.
    """

    email: str
    enable: bool = True
    uuid: int | str = Field(alias="id")

    inbound_id: int | None = Field(default=None, alias="inboundId")
    up: int = 0
    down: int = 0
    expiry_time: int = Field(default=0, alias="expiryTime")
    total: int = 0
    reset: int = 0

    flow: str = ""
    limit_ip: int = Field(default=0, alias="limitIp")
    sub_id: str = Field(default="", alias="subId")
    tg_id: str = Field(default="", alias="tgId")
    total_gb: int = Field(default=0, alias="totalGB")

    model_config = ConfigDict(populate_by_name=True)

    def to_json(self) -> dict[str, int | str | None]:
        """
        Converts the `Client` instance into a JSON-compatible dictionary.

        Returns:
            dict[str, int | str | None]: JSON-compatible dictionary representation.
        """
        return self.model_dump(by_alias=True)
