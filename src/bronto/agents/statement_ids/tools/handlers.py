import uuid
from typing import Dict

from pydantic import Field
from typing_extensions import Annotated

from bronto.agents.playbooks import compose_playbook, resolve_playbook
from bronto.clients import BrontoClient


class StatementIdsToolHandlers:
    """Statement ID generation, extraction, and deployment handlers."""

    bronto_client: BrontoClient

    @staticmethod
    def create_stmt_id() -> Annotated[
        str,
        Field(
            description="A statement ID, i.e. a 16 character long string that can "
            "be used to uniquely identify a log statement"
        ),
    ]:
        """Generate a random statement ID.

        Returns
        -------
        str
            A 16-character statement ID.
        """
        return uuid.uuid4().hex[:16]

    @staticmethod
    def inject_stmt_ids(
        src_path: Annotated[
            str,
            Field(
                description="The path to the source code where statement IDs should be "
                "injected into"
            ),
        ],
    ) -> Annotated[
        str,
        Field(description="A playbook indicating how to inject IDs in log statements"),
    ]:
        """Build the inject-statement-ID playbook.

        Parameters
        ----------
        src_path : str
            Source code root path.

        Returns
        -------
        str
            Injection playbook text.
        """
        return compose_playbook(
            "bronto.agents.statement_ids",
            "playbooks/inject_stmt_ids_playbook.md",
            src_path=src_path,
        )

    @staticmethod
    def extract_stmt_ids(
        stmt_id_filepath: Annotated[
            str,
            Field(
                description=(
                    "Output CSV path for extracted statement IDs and log statements."
                ),
                min_length=1,
            ),
        ] = "statementIds.csv",
    ) -> Annotated[
        str,
        Field(
            description="A playbook that describes how to extract statement IDs from code in order "
            "to create a mapping between these IDs and their corresponding log "
            "statements"
        ),
    ]:
        """Build the extract-statement-ID playbook.

        Parameters
        ----------
        stmt_id_filepath : str, default="statementIds.csv"
            CSV output path for extracted statement IDs.

        Returns
        -------
        str
            Extraction playbook text.
        """
        return compose_playbook(
            "bronto.agents.statement_ids",
            "playbooks/extract_stmt_ids_playbook.md",
            stmt_id_filepath=stmt_id_filepath,
        )

    @staticmethod
    def update_stmt_ids(
        src_path: Annotated[
            str,
            Field(
                description="Source code root path where statement IDs should be managed.",
                min_length=1,
            ),
        ],
        stmt_id_filepath: Annotated[
            str,
            Field(
                description=(
                    "CSV path used to store extracted and updated statement ID mappings."
                ),
                min_length=1,
            ),
        ] = "statementIds.csv",
    ) -> Annotated[
        str,
        Field(
            description="A playbook that describes how to update the statements file associated to "
            "this project."
        ),
    ]:
        """Build the update-statement-ID playbook.

        Parameters
        ----------
        src_path : str
            Source code root path.
        stmt_id_filepath : str, default="statementIds.csv"
            CSV path for statement ID mappings.

        Returns
        -------
        str
            Update playbook text.
        """
        return compose_playbook(
            "bronto.agents.statement_ids",
            "playbooks/update_stmt_ids_playbook.md",
            src_path=src_path,
            stmt_id_filepath=stmt_id_filepath,
            inject_playbook=StatementIdsToolHandlers.inject_stmt_ids(src_path),
            extract_playbook=StatementIdsToolHandlers.extract_stmt_ids(
                stmt_id_filepath
            ),
        )

    @staticmethod
    def statement_ids_playbook() -> Annotated[
        str,
        Field(
            description=(
                "A high-level playbook describing end-to-end statement ID workflow."
            )
        ),
    ]:
        """Return the statement-ID workflow playbook.

        Returns
        -------
        str
            Statement ID workflow playbook text.
        """
        return resolve_playbook(
            "bronto.agents.statement_ids", "playbooks/statement_ids_playbook.md"
        )

    def deploy_statements(
        self,
        csv_file_path: Annotated[
            str,
            Field(
                description="The path to the file containing the mapping between the log statements of the project and "
                "their corresponding statement IDs."
            ),
        ],
        project_id: Annotated[
            str,
            Field(
                description="This project ID, typically the artifact ID for a Maven project, the module name for a "
                "python project, or the Git repository name."
            ),
        ],
        version: Annotated[
            str, Field(description="The current version of this project")
        ],
        repo_url: Annotated[
            str,
            Field(
                description="The Git repository URL. This is the https URL. This can be inferred from the `git remote` "
                "command"
            ),
        ],
    ) -> Annotated[
        Dict[str, bool],
        Field(
            description="Sends to Bronto the list of log statements in this project with "
            "their corresponding statement IDs and returns whether this was "
            "performed successfully."
        ),
    ]:
        """Deploy statement-ID mappings to Bronto.

        Parameters
        ----------
        csv_file_path : str
            Path to the statement ID CSV file.
        project_id : str
            Project identifier.
        version : str
            Project version.
        repo_url : str
            HTTPS Git repository URL.

        Returns
        -------
        dict[str, bool]
            Deployment result payload.
        """
        return self.bronto_client.deploy_statements(
            csv_file_path, project_id, version, repo_url
        )
