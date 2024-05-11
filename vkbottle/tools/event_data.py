from typing import Literal, Optional

from pydantic import BaseModel, Field


class ShowSnackbarEvent(BaseModel):
    type: Literal["show_snackbar"] = "show_snackbar"
    text: str


class OpenLinkEvent(BaseModel):
    # type: str = Field(default="open_link", const=True)
    type: Literal["open_link"] = "open_link"
    link: str


class OpenAppEvent(BaseModel):
    # type: str = Field(default="open_app", const=True)
    type: Literal["open_app"] = "open_app"
    owner_id: Optional[int] = None
    app_id: int
    hash: str


__all__ = (
    "OpenAppEvent",
    "OpenLinkEvent",
    "ShowSnackbarEvent",
)
