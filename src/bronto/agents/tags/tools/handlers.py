from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import TagByNameInput, TagCreateInput, TagUpdateInput


class TagsToolHandlers:
    """Tag handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_tags(
        self,
    ) -> Annotated[dict[str, Any], Field(description="Tags payload.")]:
        """List tags.

        Returns
        -------
        dict[str, Any]
            Tag list response payload.
        """
        return self.bronto_client.list_tags()

    def create_tag(
        self,
        payload: Annotated[TagCreateInput, Field(description="Tag creation payload.")],
    ) -> Annotated[dict[str, Any], Field(description="Created tag payload.")]:
        """Create a tag.

        Parameters
        ----------
        payload : TagCreateInput
            Structured tag creation payload.

        Returns
        -------
        dict[str, Any]
            Created tag response payload.
        """
        return self.bronto_client.create_tag(payload.payload)

    def update_tag(
        self,
        payload: Annotated[TagUpdateInput, Field(description="Tag update payload.")],
    ) -> Annotated[dict[str, Any], Field(description="Updated tag payload.")]:
        """Update a tag.

        Parameters
        ----------
        payload : TagUpdateInput
            Structured tag update payload.

        Returns
        -------
        dict[str, Any]
            Updated tag response payload.
        """
        return self.bronto_client.update_tag(payload.tag_name, payload.payload)

    def delete_tag(
        self, payload: Annotated[TagByNameInput, Field(description="Tag name payload.")]
    ) -> Annotated[dict[str, Any], Field(description="Tag deletion result.")]:
        """Delete a tag.

        Parameters
        ----------
        payload : TagByNameInput
            Structured payload containing a tag name.

        Returns
        -------
        dict[str, Any]
            Tag deletion result payload.
        """
        return self.bronto_client.delete_tag(payload.tag_name)
