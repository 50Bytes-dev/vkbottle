from enum import Enum
from typing import Any

from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class BaseStateGroup(str, Enum):
    def __str__(self) -> str:
        return get_state_repr(self)


def get_state_repr(state: BaseStateGroup) -> str:
    return f"{state.__class__.__name__}:{state.value}"


class StateRepresentation(str):
    def __eq__(self, __x: object) -> bool:
        if isinstance(__x, BaseStateGroup):
            return self == get_state_repr(__x)
        return super().__eq__(__x)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
        )

    @classmethod
    def _validate(cls, v: Any) -> "StateRepresentation":
        if isinstance(v, BaseStateGroup):
            return cls(v)
        elif isinstance(v, str):
            return cls(v)
        raise ValueError(f"State value must be `string` or `BaseStateGroup`, got `{type(v)}`")


class StatePeer(BaseModel):
    peer_id: int
    state: StateRepresentation
    payload: dict = {}
