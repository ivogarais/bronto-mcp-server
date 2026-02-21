from functools import lru_cache
from importlib import resources
from string import Template


@lru_cache(maxsize=32)
def resolve_playbook(package: str, resource_path: str) -> str:
    try:
        content = (
            resources.files(package).joinpath(resource_path).read_text(encoding="utf-8")
        )
    except (FileNotFoundError, ModuleNotFoundError, OSError) as exc:
        raise RuntimeError(
            f"Cannot load playbook '{resource_path}' from package '{package}'."
        ) from exc
    return content.strip()


def compose_playbook(package: str, resource_path: str, **context: str) -> str:
    return Template(resolve_playbook(package, resource_path)).safe_substitute(context)
