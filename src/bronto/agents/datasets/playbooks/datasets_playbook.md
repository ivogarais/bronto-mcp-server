Datasets playbook:
1) Resolve dataset IDs first: use get_datasets or get_datasets_by_name.
2) Validate key names with get_keys(log_id) before building filters or grouping.
3) Validate candidate values with get_key_values(key, log_id) for string predicates.
4) Build filters using SQL WHERE syntax:
   - keys are double-quoted, e.g. "service"
   - strings are single-quoted, e.g. 'api'
   - numbers are unquoted, e.g. 500
5) If a key or value is missing, return a constrained alternative instead of guessing.
