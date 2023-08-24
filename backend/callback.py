from typing import Any
from langchain.callbacks.base import AsyncCallbackHandler
from sceemas import ChatResponse


class StreamingLLMCallbackHandler(AsyncCallbackHandler):
    def __init__(self, websocket):
        self.websocket = websocket

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        resp = ChatResponse(sender='bot', message=token, type='stream')
        await self.websocket.send_json(resp.dict())
