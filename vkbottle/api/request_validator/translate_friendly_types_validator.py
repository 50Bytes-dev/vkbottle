from pydantic import BaseModel

from enum import Enum

from vkbottle.modules import json

from .abc import ABCRequestValidator


class TranslateFriendlyTypesRequestValidator(ABCRequestValidator):
    async def validate(self, request: dict) -> dict:
        for k, v in request.copy().items():
            if isinstance(v, list):
                request[k] = ",".join(e.value if isinstance(e, Enum) else str(e) for e in v)
            elif isinstance(v, bool):
                request[k] = int(v)
            elif isinstance(v, BaseModel):
                request[k] = v.model_dump_json(exclude_none=True)
            elif isinstance(v, dict):
                request[k] = json.dumps(await self.validate(v))
            elif v is None:
                request.pop(k)
        return request
