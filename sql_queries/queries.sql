SELECT s.*, mh.day, mh.start_time_local, mh.end_time_local, tz.timezone_str
FROM store_status AS s LEFT JOIN menu_hours AS mh ON s.store_id = mh.store_id
    LEFT JOIN time_zone AS tz ON mh.store_id = tz.store_id;

SELECT
    s.store_id, mh.day, mh.end_time_local, mh.start_time_local
FROM
    store_status AS s
LEFT JOIN menu_hours AS mh ON s.store_id = mh.store_id
LEFT JOIN time_zone AS tz ON mh.store_id = tz.store_id
GROUP BY
    store_id, mh.day, mh.end_time_local, mh.start_time_local;