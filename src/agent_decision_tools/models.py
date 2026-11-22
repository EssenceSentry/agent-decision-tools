"""Common model conventions for the calculation API."""

from abc import ABC, abstractmethod
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, FiniteFloat

Name = Annotated[str, Field(min_length=1)]
Probability = Annotated[FiniteFloat, Field(ge=0, le=1)]
Nonnegative = Annotated[FiniteFloat, Field(ge=0)]


class Inputs(BaseModel):
    """Require explicit fields and finite numerical values."""

    model_config = ConfigDict(
        extra="forbid", strict=True, allow_inf_nan=False, str_strip_whitespace=True
    )


class Request(Inputs, ABC):
    """An operation and the provenance of its numerical inputs."""

    basis: Name = Field(
        description="Source records, grounded assumptions or synthetic example."
    )

    @abstractmethod
    def calculate(self) -> dict[str, object]:
        """Return the operation's numerical results and decision details."""
