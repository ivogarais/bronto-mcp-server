from functools import lru_cache
from importlib import resources
from string import Template


@lru_cache(maxsize=32)
def resolve_playbook(package: str, resource_path: str) -> str:
    """Load a playbook resource from a package.

    Parameters
    ----------
    package : str
        Python package path.
    resource_path : str
        Relative resource file path.

    Returns
    -------
    str
        Playbook content.
    """
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
    """Render a playbook template with string context values.

    Parameters
    ----------
    package : str
        Python package path.
    resource_path : str
        Relative template file path.
    **context : str
        Template substitution values.

    Returns
    -------
    str
        Rendered playbook content.
    """
    return Template(resolve_playbook(package, resource_path)).safe_substitute(context)
