import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from pydantic import Field, ValidationError
from typing_extensions import Annotated

from bronto.agents.playbooks import resolve_playbook
from bronto.logger import module_logger
from bronto.schemas import DashboardBuildInput, build_bronto_app_spec

logger = module_logger(__name__)


class DashboardToolHandlers:
    """Dashboard spec generation and Bronto CLI launch handlers."""

    @staticmethod
    def build_dashboard_spec(
        payload: Annotated[
            dict[str, Any],
            Field(
                description=(
                    "Simplified dashboard payload. Required shape: "
                    "{title, density?, bar_charts?, tables?}. "
                    "Use bar_charts[] and/or tables[] (not widgets/chart)."
                )
            ),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="A validated full Bronto dashboard spec JSON object."),
    ]:
        request = _validate_payload(payload)
        return build_bronto_app_spec(request)

    @staticmethod
    def serve_dashboard(
        payload: Annotated[
            dict[str, Any],
            Field(
                description=(
                    "Simplified dashboard payload. Required shape: "
                    "{title, density?, bar_charts?, tables?}. "
                    "Use bar_charts[] and/or tables[] (not widgets/chart)."
                )
            ),
        ],
        keep_spec_file: Annotated[
            bool,
            Field(
                description=(
                    "If true, keep the generated spec JSON on disk for inspection. "
                    "If false, remove it after successful exit."
                )
            ),
        ] = False,
        spec_file_path: Annotated[
            str | None,
            Field(
                description=(
                    "Optional path where generated spec JSON will be written. "
                    "When provided, file is always kept."
                )
            ),
        ] = None,
    ) -> Annotated[
        dict[str, Any],
        Field(
            description=(
                "Result metadata for Bronto launch, including the command and the "
                "spec file path."
            )
        ),
    ]:
        request = _validate_payload(payload)
        app_spec = build_bronto_app_spec(request)
        spec_path = _write_spec_file(app_spec, spec_file_path)

        bronto_bin = _resolve_bronto_binary()
        command = [bronto_bin, "serve", "--spec", str(spec_path)]
        logger.info("Launching Bronto dashboard, command=%s", command)

        try:
            completed = subprocess.run(command, check=False)
        except OSError as exc:
            raise RuntimeError(
                f"Failed to execute Bronto CLI using command: {' '.join(command)}"
            ) from exc

        if completed.returncode != 0:
            raise RuntimeError(
                "`bronto serve` failed with exit code "
                f"{completed.returncode}. Command: {' '.join(command)}"
            )

        retained = keep_spec_file or spec_file_path is not None
        if not retained:
            spec_path.unlink(missing_ok=True)

        return {
            "status": "ok",
            "command": command,
            "spec_path": str(spec_path),
            "spec_retained": retained,
            "exit_code": completed.returncode,
        }

    @staticmethod
    def dashboard_playbook() -> Annotated[
        str,
        Field(
            description=(
                "Playbook with exact payload contract and examples for "
                "build_dashboard_spec and serve_dashboard."
            )
        ),
    ]:
        return resolve_playbook(
            "bronto.agents.dashboard", "playbooks/dashboard_playbook.md"
        )


def _write_spec_file(spec_document: dict[str, Any], spec_file_path: str | None) -> Path:
    if spec_file_path:
        path = Path(spec_file_path).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        fd, temp_path = tempfile.mkstemp(prefix="bronto-spec-", suffix=".json")
        os.close(fd)
        path = Path(temp_path)

    path.write_text(json.dumps(spec_document, indent=2), encoding="utf-8")
    return path


def _validate_payload(payload: dict[str, Any]) -> DashboardBuildInput:
    try:
        return DashboardBuildInput.model_validate(payload)
    except ValidationError as exc:
        raise ValueError(
            "Invalid dashboard payload. Top-level shape must be: "
            "{title, density?, bar_charts?, tables?}. "
            "Use `dashboard_playbook` for exact examples. "
            f"Validation details: {exc}"
        ) from exc


def _resolve_bronto_binary() -> str:
    configured = os.environ.get("BRONTO_BIN", "bronto").strip() or "bronto"
    if os.path.sep in configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_file():
            raise RuntimeError(
                f"BRONTO_BIN points to a missing file: {candidate}. "
                "Install bronto or update BRONTO_BIN."
            )
        return str(candidate)

    resolved = shutil.which(configured)
    if resolved is None:
        raise RuntimeError(
            "Could not find `bronto` in PATH. Install Bronto CLI or set BRONTO_BIN to the full binary path."
        )
    return resolved
