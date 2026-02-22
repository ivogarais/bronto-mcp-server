Compute metrics playbook:
1) Always provide log_ids and a bounded time range.
   timerange_start/timerange_end accept unix ms or UTC "YYYY-MM-DD HH:mm:ss".
2) metric_functions must use Bronto syntax, e.g. COUNT(*), AVG("latency_ms"), SUM("bytes").
3) Validate metric keys and group_by_keys with get_keys(log_id) before running.
4) Use group_by_keys only when you need split series; otherwise leave it empty for totals.
5) After detecting anomalies, follow up with search_logs on the same group/filter window.
