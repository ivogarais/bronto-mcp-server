Search logs playbook:
1) Always provide log_ids (dataset IDs) explicitly.
2) Prefer explicit timerange_start and timerange_end in unix ms (UTC).
   Use get_timestamp_as_unix_epoch to convert YYYY-MM-DD HH:mm:ss.
3) Before using a filter, validate keys via get_keys(log_id).
4) Filter syntax rules:
   - keys are double-quoted
   - string values are single-quoted
   - numeric values are unquoted
5) Start with a narrow time window and expand only if needed.
