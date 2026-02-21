import uuid
from typing import Dict

from pydantic import Field
from typing_extensions import Annotated


class StatementIdsToolHandlers:
    """Statement ID generation, extraction, and deployment handlers."""

    @staticmethod
    def create_stmt_id() -> Annotated[
        str,
        Field(
            description="A statement ID, i.e. a 16 character logn string that can "
            "be used to uniquely identify a log statement"
        ),
    ]:
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
        Field(description="A prompt indicating how to inject IDs in log statements"),
    ]:
        return f"""A statement ID is a string of characters that uniquely identify a log statement. In order to inject 
        statement IDs, simply update log statements by appending ' stmt_id=<STMT_ID>'. The value of STMT_ID should be 
        constant and unique per log statement. Below are examples of log statements, based on the Python programming 
        language, before and after injecting statement IDs:
        logger.info('a simple log statement') --> logger.info('a simple log statement stmt_id=8320e3c149f34c28')
        logger.info('a log statement with a placeholder %s', value) --> logger.info('a log statement with a placeholder %s stmt_id=be7e775bbaf949a3', value)
        logger.info(expr_representing_a_string) --> logger.info(expr_representing_a_string + ' stmt_id=e0c64be98903425a')
        logger.info('a multiline ' + 
                    'log statement') --> logger.info('a multiline ' + 
                                                     'log statement stmt_id=12fd106cdffc4a09')  
        If structured logging is used in the codebase, such as using the `extra` parameter in Python or the Fluent 
        logging API in Java, then the same pattern should be used to inject statement IDs, e.g. in Python         

        logger.info('a simple log statement') --> logger.info('a simple log statement', extra={{'stmt_id': '8320e3c149f34c28'}})

        and in Java with the Fluent API:
        
        logger.atInfo().setMessage("a simple log statement").log() --> logger.atInfo().setMessage("a simple log statement").addKeyValue("stmt_id, "8320e3c149f34c28").log()

        Also, check available tools that generate statement IDs.
        Finally, the following applies:
        - Statement IDs should only be injected into source code located under {src_path} 
        - Only one statement ID should be defined per log statement.
        - Statement IDs should be injected in log statement messages, regardless of the severity of the log statement
        - Event though the samples above focus on the Python programming language, statement IDs should be injected 
        regardless of the programming language used.
        """

    @staticmethod
    def extract_stmt_ids(
        stmt_id_filepath: str = "statementIds.csv",
    ) -> Annotated[
        str,
        Field(
            description="A prompt that describes how to extract statement IDs from code in order "
            "to create a mapping between these IDs and their corresponding log "
            "statements"
        ),
    ]:
        return f"""The messages of log statements in this project contain a key-value pair where the key name is 
          stmt_id. Can you please extract the value associated to each statement ID and associated it to the log 
          statement itself, as well as the file path and line number where the log statement is located? For instance, 
          if the message of the log statement is 
          
          'this is a %s statement, stmt_id=1234567890'
          
          then extracting the statement ID and log statement should lead to 
          
          1234567890,"this is a %s statement, stmt_id=1234567890",path/to/file,34
          
          If the log message is a concatenation of strings, then please use the 
          evaluated string as log statement, i.e. extracting 
          
          'this is a %s' + ' statement, stmt_id=1234567890'
          
          should lead to 
          
          1234567890,"this is a %s statement, stmt_id=1234567890",path/to/file,34
          
          Finally, if the log statement contains non evaluated string, please replace these 
          parts with %s, for instance extracting 
          
          'this is a %s ' + str(my_object) + ' statement, stmt_id=1234567890'
          
          should lead to 
          
          1234567890,"this is a %s %s statement stmt_id=1234567890",path/to/file,34 
          
          Write all the extracted log statements and statement IDs to a CSV file named {stmt_id_filepath} at 
          the root of this project. This CSV file should contain the following headers: 
          statement_id,log_statement,file_path,line_number
          where 
          - statement_id is the stmt_id value of the log statement
          - log_statement is the log statement message itself
          - is the file where the log statement is located
          - line_number is the line number where the log statement is defined
          """

    @staticmethod
    def update_stmt_ids(
        src_path: str, stmt_id_filepath: str = "statementIds.csv"
    ) -> Annotated[
        str,
        Field(
            description="A prompt that describes how to update the statements file associated to "
            "this project."
        ),
    ]:
        return f"""Updating statement IDs consists of injecting statement IDs in log statements where they would be 
        missing as well as updating the details in {stmt_id_filepath} for log statements for which information would have 
        changed, e.g. filepath or line number would have changed. Descriptions on how to inject and extract statement 
        IDs are provided below:
        
        # Injecting Statement IDS
        {StatementIdsToolHandlers.inject_stmt_ids(src_path)}
        
        # Extracting Lost Statements - Updating {stmt_id_filepath}
        {StatementIdsToolHandlers.extract_stmt_ids(stmt_id_filepath)}
        """

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
        Dict,
        Field(
            description="Sends to Bronto the list of log statements in this project with "
            "their corresponding statement IDs and returns whether this was "
            "performed successfully."
        ),
    ]:
        return self.bronto_client.deploy_statements(
            csv_file_path, project_id, version, repo_url
        )
