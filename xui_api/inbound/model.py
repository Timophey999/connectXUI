"""
This module defines the base classes for inbound models in the XUI API.
"""

import json
from typing import Any
from pydantic import BaseModel, model_validator


class JsonModel(BaseModel):
    """
    Base class for models that include a JSON string field.

    Provides functionality to automatically convert JSON strings to dictionaries
    during validation.

    Methods:
        model_validate(cls, values): Validates and processes input values.
    """

    @model_validator(mode="before")
    def model_validate(cls, values: Any) -> Any:
        """
        Validates the input values and converts JSON strings to dictionaries if necessary.

        Args:
            values (Any): The input values to validate.

        Returns:
            Any: The processed values.
        """
        if isinstance(values, str):
            try:
                return json.loads(values)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON string: {values}") from exc
        return values
