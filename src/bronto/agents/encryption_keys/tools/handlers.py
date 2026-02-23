from typing import Any

from pydantic import Field
from typing_extensions import Annotated

from bronto.clients import BrontoClient
from bronto.schemas import (
    EncryptionKeyByIdInput,
    EncryptionKeyCreateInput,
    EncryptionKeyUpdateInput,
)


class EncryptionKeysToolHandlers:
    """Encryption key handlers exposed as MCP tools."""

    bronto_client: BrontoClient

    def list_encryption_keys(
        self,
    ) -> Annotated[
        list[dict[str, Any]], Field(description="Encryption key list payload.")
    ]:
        """List encryption keys.

        Returns
        -------
        list[dict[str, Any]]
            Encryption key list response payload.
        """
        return self.bronto_client.list_encryption_keys()

    def create_encryption_key(
        self,
        payload: Annotated[
            EncryptionKeyCreateInput,
            Field(description="Encryption key creation payload."),
        ],
    ) -> Annotated[
        dict[str, Any], Field(description="Created encryption key payload.")
    ]:
        """Create an encryption key.

        Parameters
        ----------
        payload : EncryptionKeyCreateInput
            Structured key creation payload.

        Returns
        -------
        dict[str, Any]
            Created encryption key payload.
        """
        return self.bronto_client.create_encryption_key(payload.payload)

    def get_encryption_key(
        self,
        payload: Annotated[
            EncryptionKeyByIdInput, Field(description="Encryption key ID payload.")
        ],
    ) -> Annotated[dict[str, Any], Field(description="Encryption key payload.")]:
        """Get encryption key details.

        Parameters
        ----------
        payload : EncryptionKeyByIdInput
            Structured payload containing an encryption key ID.

        Returns
        -------
        dict[str, Any]
            Encryption key details payload.
        """
        return self.bronto_client.get_encryption_key(payload.encryption_key_id)

    def update_encryption_key(
        self,
        payload: Annotated[
            EncryptionKeyUpdateInput,
            Field(description="Encryption key update payload."),
        ],
    ) -> Annotated[
        dict[str, Any], Field(description="Updated encryption key payload.")
    ]:
        """Update an encryption key.

        Parameters
        ----------
        payload : EncryptionKeyUpdateInput
            Structured key update payload.

        Returns
        -------
        dict[str, Any]
            Updated encryption key payload.
        """
        return self.bronto_client.update_encryption_key(
            payload.encryption_key_id, payload.payload
        )

    def delete_encryption_key(
        self,
        payload: Annotated[
            EncryptionKeyByIdInput, Field(description="Encryption key ID payload.")
        ],
    ) -> Annotated[
        dict[str, Any], Field(description="Encryption key deletion result.")
    ]:
        """Delete an encryption key.

        Parameters
        ----------
        payload : EncryptionKeyByIdInput
            Structured payload containing an encryption key ID.

        Returns
        -------
        dict[str, Any]
            Encryption key deletion result payload.
        """
        return self.bronto_client.delete_encryption_key(payload.encryption_key_id)
