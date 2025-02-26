{{ config(materialized='table') }}

with fhv_trips_data as (
    select 
        PUlocationid,
        pickup_year,
        pickup_month,
        pickup_borough,
        pickup_zone,
        DOlocationid,
        dropoff_borough,
        dropoff_zone,
        TIMESTAMP_DIFF(dropOff_datetime, pickup_datetime, SECOND) as trip_duration
    from {{ ref('dim_fhv_trips') }}
)

select 
    *,
    PERCENTILE_CONT(trip_duration, 0.90) OVER
    (PARTITION BY pickup_year, pickup_month, PUlocationid, DOlocationid) AS p90_duration  -- 90th percentile
from fhv_trips_data