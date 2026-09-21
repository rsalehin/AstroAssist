"""Deterministic mock model provider [F-EVAL-001].

Replays scripted responses so every unit/e2e run is offline and key-free (docs/TESTING.md).
A response is chosen by reasoning role and, optionally, a substring that must appear in the
prompt (``match``) — the first matching entry for the role wins, else a default per role.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import BaseModel

from astroassist.core.models.base import ModelRole


class MockResponse(BaseModel):
    role: str
    text: str
    match: str | None = None


class MockScript(BaseModel):
    responses: list[MockResponse]

    @classmethod
    def from_yaml(cls, path: Path) -> MockScript:
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        return cls.model_validate(data)

    def response_for(self, role: str, prompt: str) -> str:
        fallback: str | None = None
        for r in self.responses:
            if r.role != role:
                continue
            if r.match is None:
                fallback = fallback if fallback is not None else r.text
            elif r.match.lower() in prompt.lower():
                return r.text
        if fallback is not None:
            return fallback
        return f"[mock:{role}] no scripted response"


DEFAULT_SCRIPT = MockScript(
    responses=[
        MockResponse(role="router", text="echo"),
        MockResponse(role="planner", text="echo"),
        MockResponse(
            role="synthesis",
            text="Echo complete — the input was echoed back as an artifact.",
        ),
    ]
)


class MockChatModel(BaseChatModel):
    """A LangChain chat model that returns scripted text for a fixed role."""

    role: str
    script: MockScript

    @property
    def _llm_type(self) -> str:
        return "astroassist-mock"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        prompt = "\n".join(str(m.content) for m in messages)
        text = self.script.response_for(self.role, prompt)
        generation = ChatGeneration(message=AIMessage(content=text))
        return ChatResult(generations=[generation])


class MockModelProvider:
    """Provider that yields :class:`MockChatModel` instances for each role."""

    def __init__(self, script: MockScript) -> None:
        self.name = "mock"
        self.script = script

    @classmethod
    def default(cls) -> MockModelProvider:
        import os

        path = os.environ.get("ASTROASSIST_MOCK_SCRIPT")
        if path and Path(path).exists():
            return cls(MockScript.from_yaml(Path(path)))
        return cls(DEFAULT_SCRIPT)

    def get_chat_model(self, role: ModelRole) -> BaseChatModel:
        return MockChatModel(role=role, script=self.script)
