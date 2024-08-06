WITH menu_hours AS (
    SELECT
        bh.store_id,
        bh.dayOfWeek,
        time_zones.timezone_str,
        bh.start_time_local,
        bh.end_time_local,
        datetime('now', '+' || (strftime('%s', bh.start_time_local) - strftime('%s', 'now')) || ' seconds', time_zones.timezone_str || ' hours') AS start_time_utc,
        datetime('now', '+' || (strftime('%s', bh.end_time_local) - strftime('%s', 'now')) || ' seconds', time_zones.timezone_str || ' hours') AS end_time_utc
    FROM
        business_hours bh
    LEFT JOIN
        time_zones ON bh.store_id = time_zones.store_id
),
StatusLastHour AS (
    SELECT
        store_id,
        timestamp_utc,
        status,
        LEAD(status) OVER (PARTITION BY store_id ORDER BY timestamp_utc) AS next_status,
        strftime('%s', LEAD(timestamp_utc) OVER (PARTITION BY store_id ORDER BY timestamp_utc)) - strftime('%s', timestamp_utc) AS interval_seconds
    FROM
        store_status
    WHERE
        timestamp_utc > datetime('now', '-1 hour')
)
SELECT
    store_id,
    SUM(CASE WHEN status = 'active' THEN interval_seconds ELSE 0 END) / 60.0 AS uptime_last_hour,
    SUM(CASE WHEN status = 'inactive' THEN interval_seconds ELSE 0 END) / 60.0 AS downtime_last_hour
FROM
    StatusLastHour
GROUP BY
    store_id;
