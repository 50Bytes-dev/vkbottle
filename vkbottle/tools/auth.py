from typing import TYPE_CHECKING, List, Optional

from vkbottle.api.api import CaptchaHandler
from vkbottle.exception_factory import CaptchaError, VKAPIError
from vkbottle.http import SingleAiohttpClient

if TYPE_CHECKING:
    from vkbottle.http import ABCHTTPClient

MOBILE_APP_ID = 2274003
MOBILE_APP_SECRET = "hHbZxrka2uZ6jB1inYsH"  # noqa: S105


class AuthError(VKAPIError[0]):  # type: ignore
    def __init__(
        self,
        *,
        error_description: str,
        error_type: str,
        error_msg: str,
        request_params: Optional[List[dict]] = None,
    ):
        request_params = request_params or []
        super().__init__(error_msg=error_msg, request_params=request_params)
        self.error_msg = error_msg
        self.error_type = error_type
        self.error_description = error_description


class UserAuth:
    AUTH_URL = "https://oauth.vk.com/token"

    def __init__(
        self,
        client_id: Optional[int] = None,
        client_secret: Optional[str] = None,
        http_client: Optional["ABCHTTPClient"] = None,
    ):
        if client_id is not None and client_secret is not None:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self.client_id = MOBILE_APP_ID
            self.client_secret = MOBILE_APP_SECRET

        self.http_client = http_client or SingleAiohttpClient()
        self.captcha_handler: Optional[CaptchaHandler] = None

    def _get_params(self, login: str, password: str) -> dict:
        return {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": login,
            "password": password,
            "scope": 501202911,
        }

    async def get_token(self, login: str, password: str, **kwargs) -> str:
        params = self._get_params(login, password)
        params.update(kwargs)

        response = await self.http_client.request_json(
            url=self.AUTH_URL,
            method="POST",
            data=params,
        )

        if "access_token" in response:
            return response["access_token"]
        response["error_msg"] = response.pop("error")
        if response["error_msg"] == "need_captcha":
            if self.captcha_handler:
                key = await self.captcha_handler(CaptchaError(**response, request_params=[]))
                return await self.get_token(
                    login,
                    password,
                    captcha_sid=response["captcha_sid"],
                    captcha_key=key,
                )
            raise CaptchaError(**response, request_params=[])
        raise AuthError(**response, request_params=[])

    def add_captcha_handler(self, handler: CaptchaHandler) -> CaptchaHandler:
        self.captcha_handler = handler
        return handler
