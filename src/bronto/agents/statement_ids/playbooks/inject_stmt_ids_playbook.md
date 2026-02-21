A statement ID is a string that uniquely identifies a log statement. To inject IDs, append `stmt_id=<STMT_ID>` to each log message and keep the value stable for that statement.

Examples:
- `logger.info('a simple log statement')` -> `logger.info('a simple log statement stmt_id=8320e3c149f34c28')`
- `logger.info('a log statement with a placeholder %s', value)` -> `logger.info('a log statement with a placeholder %s stmt_id=be7e775bbaf949a3', value)`
- `logger.info(expr_representing_a_string)` -> `logger.info(expr_representing_a_string + ' stmt_id=e0c64be98903425a')`
- `logger.info('a multiline ' + 'log statement')` -> `logger.info('a multiline ' + 'log statement stmt_id=12fd106cdffc4a09')`

Structured logging should follow the same principle:
- Python `extra`: `logger.info('a simple log statement', extra={'stmt_id': '8320e3c149f34c28'})`
- Java fluent logging: `logger.atInfo().setMessage("a simple log statement").addKeyValue("stmt_id", "8320e3c149f34c28").log()`

Rules:
- Inject IDs only under `${src_path}`.
- Exactly one statement ID per log statement.
- Apply across all severities.
- Apply regardless of language.
