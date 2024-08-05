# Store Monitoring

This project is designed to monitor the uptime and downtime of stores based on their business hours and status polls. The goal is to generate reports detailing the store's uptime and downtime over various time intervals (last hour, last day, and last week).

## Data Sources

1. **Store Status Data**:
   - Contains information about whether the store was active or inactive.
   - Schema: `store_id, timestamp_utc, status`
   - Timestamps are in UTC.

2. **Business Hours Data**:
   - Contains the business hours for each store.
   - Schema: `store_id, dayOfWeek (0=Monday, 6=Sunday), start_time_local, end_time_local`
   - Times are in the local timezone.

3. **Time Zone Data**:
   - Contains the timezone for each store.
   - Schema: `store_id, timezone_str`
   - If data is missing, assume the timezone is `America/Chicago`.

## Objectives

- Calculate the uptime and downtime of stores within their business hours.
- Generate a report with the following schema:
  - `store_id, uptime_last_hour (in minutes), uptime_last_day (in hours), uptime_last_week (in hours), downtime_last_hour (in minutes), downtime_last_day (in hours), downtime_last_week (in hours)`

## Assumptions

- If business hours data is missing for a store, assume it is open 24/7.
- Uptime and downtime calculations should only include observations within business hours.
- Extrapolate uptime and downtime based on the periodic polls.


## My ongoing work

- since, the smallest unit for which we have to measure the availability is an hour.
- we divide menu_hours into batches of 1 hour for each day. (eg: 9AM to 12PM contains 3 batches).
- we look for available data in each of the batches.
- if the store was active we mark the whole hour as available. 
- if the store was not active or the data is not available then we mark the whole hour as not available.