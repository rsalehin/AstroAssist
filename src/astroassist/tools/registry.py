"""Tool registry [F-AG-016].

Curated, typed tools are registered with a domain, a risk class (drives preflight/HITL) and an
optional cost estimator (drives preflight estimates). The registry auto-exposes the LangChain
tools to agents and lets the planner reason about cost and risk before executing a step.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel

RiskClass = Literal["safe", "query", "download", "code", "destructive"]

CostEstimate = dict[str, Any]
CostEstimator = Callable[..., CostEstimate]


@dataclass
class ToolSpec:
    name: str
    tool: BaseTool
    func: Callable[..., Any]
    domain: str
    risk_class: RiskClass
    cost_estimator: CostEstimator | None = None

    def estimate(self, **kwargs: Any) -> CostEstimate:
        if self.cost_estimator is None:
            return {"queries": 0, "est_rows": 0, "est_bytes": 0, "est_seconds": 0}
        return self.cost_estimator(**kwargs)


class ToolRegistry:
    def __init__(self) -> None:
        self._specs: dict[str, ToolSpec] = {}

    def register(
        self,
        func: Callable[..., Any],
        *,
        name: str,
        description: str,
        args_schema: type[BaseModel],
        domain: str,
        risk_class: RiskClass,
        cost_estimator: CostEstimator | None = None,
    ) -> ToolSpec:
        tool = StructuredTool.from_function(
            func=func, name=name, description=description, args_schema=args_schema
        )
        spec = ToolSpec(
            name=name,
            tool=tool,
            func=func,
            domain=domain,
            risk_class=risk_class,
            cost_estimator=cost_estimator,
        )
        self._specs[name] = spec
        return spec

    def get(self, name: str) -> ToolSpec:
        return self._specs[name]

    def has(self, name: str) -> bool:
        return name in self._specs

    def all(self) -> list[ToolSpec]:
        return list(self._specs.values())

    def by_domain(self, domain: str) -> list[ToolSpec]:
        return [s for s in self._specs.values() if s.domain == domain]

    def tools(self) -> list[BaseTool]:
        return [s.tool for s in self._specs.values()]


# Process-wide default registry; connectors/tools register into it at import.
default_registry = ToolRegistry()
