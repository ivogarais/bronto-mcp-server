Updating statement IDs means:
- injecting missing statement IDs in source logs
- refreshing `${stmt_id_filepath}` for moved/changed statements

# Inject Statement IDs
${inject_playbook}

# Extract and Refresh CSV
${extract_playbook}
