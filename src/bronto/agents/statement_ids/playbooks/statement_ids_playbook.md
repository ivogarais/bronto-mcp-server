Statement IDs playbook:
1) Generate IDs with create_stmt_id when a stable ID is needed for a new log statement.
2) Inject IDs consistently with inject_stmt_ids(src_path) so each log statement has exactly one stmt_id.
3) Extract mappings with extract_stmt_ids(stmt_id_filepath) to keep the CSV inventory current.
4) Use update_stmt_ids(src_path, stmt_id_filepath) to reconcile both injection and extraction after code changes.
5) Deploy statement metadata with deploy_statements(csv_file_path, project_id, version, repo_url).
6) Never change an existing statement ID unless the log statement semantic meaning changed.
