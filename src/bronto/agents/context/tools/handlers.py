from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import ContextQueryInput


class ContextToolHandlers:
    """Context handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def get_context(
        self,
        payload: Annotated[
            ContextQueryInput,
            Field(
                description=(
                    "Context query payload with optional selectors: "
                    "{from?, from_tags?, from_expr?, sequence?, timestamp?, "
                    "direction?, limit?, explain?}."
                )
            ),
        ],
    ) -> Annotated[
        dict[str, Any],
        Field(description="Raw context response payload returned by Bronto."),
    ]:
        return self.bronto_client.get_context(
            from_=payload.from_,
            from_tags=payload.from_tags,
            from_expr=payload.from_expr,
            sequence=payload.sequence,
            timestamp=payload.timestamp,
            direction=payload.direction,
            limit=payload.limit,
            include_explain=payload.include_explain,
        )
