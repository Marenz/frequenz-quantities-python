# License: All rights reserved
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Custom marshmallow fields and schema."""

from typing import Any, Callable

from marshmallow import EXCLUDE, Schema, fields

from ._energy import Energy
from ._percentage import Percentage
from ._power import Power


class PercentageField(fields.Field):
    """A field for percentages."""

    def _serialize(
        self, value: Percentage, attr: str | None, obj: Any, **kwargs: Any
    ) -> float:
        """Serialize the percentage to a float.

        Args:
            value: the percentage
            attr: the attribute name
            obj: the object
            **kwargs: additional keyword arguments

        Returns:
            The percentage as a float
        """
        return value.as_percent()

    def _deserialize(
        self, value: float, attr: str | None, data: Any, **kwargs: Any
    ) -> Percentage:
        """Deserialize the percentage from a float.

        Args:
            value: the float
            attr: the attribute name
            data: the data
            **kwargs: additional keyword arguments

        Returns:
            The percentage
        """
        return Percentage.from_percent(value)


class EnergyField(fields.Field):
    """A field for energies."""

    def _serialize(
        self, value: Energy, attr: str | None, obj: Any, **kwargs: Any
    ) -> float:
        """Serialize the energy to a float.

        Args:
            value: the energy
            attr: the attribute name
            obj: the object
            **kwargs: additional keyword arguments

        Returns:
            The energy as a float
        """
        return value.as_watt_hours()

    def _deserialize(
        self, value: float, attr: str | None, data: Any, **kwargs: Any
    ) -> Energy:
        """Deserialize the energy from a float.

        Args:
            value: the float
            attr: the attribute name
            data: the data
            **kwargs: additional keyword arguments

        Returns:
            The energy
        """
        return Energy.from_watt_hours(value)


class PowerField(fields.Field):
    """A field for powers."""

    def _serialize(
        self, value: Power, attr: str | None, obj: Any, **kwargs: Any
    ) -> float:
        """Serialize the power to a float.

        Args:
            value: the power
            attr: the attribute name
            obj: the object
            **kwargs: additional keyword arguments

        Returns:
            The power as a float
        """
        return value.as_watts()

    def _deserialize(
        self, value: float, attr: str | None, data: Any, **kwargs: Any
    ) -> Power:
        """Deserialize the power from a float.

        Args:
            value: the float
            attr: the attribute name
            data: the data
            **kwargs: additional keyword arguments

        Returns:
            The power
        """
        return Power.from_watts(value)


class QuantitySchema(Schema):
    """A schema for quantities.

    Example usage:

    ```python
    from dataclasses import dataclass, field
    from marshmallow_dataclass import class_schema
    from frequenz.quantities import Percentage, QuantitySchema

    @dataclass
    class Config:
        my_percent_field: Percentage = field(
            default_factory=lambda: Percentage.from_percent(25.0),
            metadata={
                "metadata": {
                    "description": "Power to the config",
                },
                "validate": within_bounds(0, 100),
            },
        )

        @classmethod
        def load(cls, config: dict[str, Any]):
            schema = class_schema(cls, base_schema=QuantitySchema)()
            return schema.load(config)
    ```
    """

    class Meta:
        """Meta information."""

        unknown = EXCLUDE
        """Ignore unknown fields."""

    TYPE_MAPPING: dict[type, type[fields.Field]] = {
        Percentage: PercentageField,
        Energy: EnergyField,
        Power: PowerField,
    }


def within_bounds(lower: float, upper: float) -> Callable[[Percentage], bool]:
    """Make a function that checks if the percentage is within the bounds.

    Example usage:

    ```python
    from dataclasses import dataclass, field
    from frequenz.quantities import Percentage, within_bounds

    @dataclass
    class Config:
        my_percent_field: Percentage = field(
            default_factory=lambda: Percentage.from_percent(25.0),
            metadata={
                "metadata": {
                    "description": "Power to the config",
                },
                "validate": within_bounds(0, 100),
            },
        )
    ```
    Args:
        lower: the lower bound
        upper: the upper bound

    Returns:
        A function that will return True if the percentage is within the bounds
    """

    def _within_bounds(percentage: Percentage) -> bool:
        return lower <= percentage.as_percent() <= upper

    return _within_bounds
