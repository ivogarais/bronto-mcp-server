from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import TagByNameInput, TagCreateInput, TagUpdateInput


class TagsToolHandlers:
    bronto_client: BrontoClient

    def list_tags(self) -> Annotated[dict[str, Any], Field(description="Tags payload.")]:
        return self.bronto_client.list_tags()

    def create_tag(self, payload: Annotated[TagCreateInput, Field(description="Tag creation payload.")]) -> Annotated[dict[str, Any], Field(description="Created tag payload.")]:
        return self.bronto_client.create_tag(payload.payload)

    def update_tag(self, payload: Annotated[TagUpdateInput, Field(description="Tag update payload.")]) -> Annotated[dict[str, Any], Field(description="Updated tag payload.")]:
        return self.bronto_client.update_tag(payload.tag_name, payload.payload)

    def delete_tag(self, payload: Annotated[TagByNameInput, Field(description="Tag name payload.")]) -> Annotated[dict[str, Any], Field(description="Tag deletion result.")]:
        return self.bronto_client.delete_tag(payload.tag_name)
