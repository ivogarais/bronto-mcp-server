Extract statement IDs (`stmt_id=...`) from log messages and produce a CSV mapping for this project.

Expected output format per row:
`statement_id,log_statement,file_path,line_number`

Examples:
- Input log message: `'this is a %s statement, stmt_id=1234567890'`
- Output row: `1234567890,"this is a %s statement, stmt_id=1234567890",path/to/file,34`

For concatenated literals, use the evaluated string:
- Input: `'this is a %s' + ' statement, stmt_id=1234567890'`
- Output: `1234567890,"this is a %s statement, stmt_id=1234567890",path/to/file,34`

For non-literal fragments, normalize unknown runtime values as `%s`:
- Input: `'this is a %s ' + str(my_object) + ' statement, stmt_id=1234567890'`
- Output: `1234567890,"this is a %s %s statement stmt_id=1234567890",path/to/file,34`

Write the CSV file to `${stmt_id_filepath}` at project root with headers:
`statement_id,log_statement,file_path,line_number`
