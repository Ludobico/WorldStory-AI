from typing import Any, List, Mapping, Optional, Union

from g4f import ChatCompletion
from g4f.models import Model
from g4f.Provider.base_provider import BaseProvider
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.llms.utils import enforce_stop_tokens


class G4FLLM(LLM):
    model: Union[Model, str]
    provider: Optional[type[BaseProvider]] = None
    auth: Optional[Union[str, bool]] = None
    create_kwargs: Optional[dict[str, Any]] = None

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        create_kwargs = {} if self.create_kwargs is None else self.create_kwargs.copy()
        create_kwargs["model"] = self.model
        if self.provider is not None:
            create_kwargs["provider"] = self.provider
        if self.auth is not None:
            create_kwargs["auth"] = self.auth

        text = ChatCompletion.create(
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **create_kwargs,
        )

        # Generator -> str
        text = text if type(text) is str else "".join(text)
        if stop is not None:
            text = enforce_stop_tokens(text, stop)
        return text

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "model": self.model,
            "provider": self.provider,
            "auth": self.auth,
            "create_kwargs": self.create_kwargs,
        }