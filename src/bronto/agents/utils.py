import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).with_name("agent_catalog.json")
TOKEN_PATTERN = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


@lru_cache(maxsize=1)
def _catalog_snapshot() -> dict[str, Any]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _render_tokens(value: Any, tokens: dict[str, str]) -> Any:
    if isinstance(value, str):
        return TOKEN_PATTERN.sub(lambda m: tokens.get(m.group(1), m.group(0)), value)
    if isinstance(value, list):
        return [_render_tokens(item, tokens) for item in value]
    if isinstance(value, dict):
        return {key: _render_tokens(item, tokens) for key, item in value.items()}
    return value


def resolve_agent_blueprint(
    agent_name: str, runtime_tokens: dict[str, str] | None = None
) -> dict[str, Any]:
    snapshot = _catalog_snapshot()
    placeholders = dict(snapshot.get("placeholders", {}))
    if runtime_tokens:
        placeholders.update(runtime_tokens)

    agents = snapshot.get("agents", {})
    if agent_name not in agents:
        raise KeyError(f"Unknown agent blueprint: {agent_name}")

    raw_blueprint = agents[agent_name]
    rendered_blueprint = _render_tokens(raw_blueprint, placeholders)
    rendered_blueprint["name"] = agent_name
    return rendered_blueprint
