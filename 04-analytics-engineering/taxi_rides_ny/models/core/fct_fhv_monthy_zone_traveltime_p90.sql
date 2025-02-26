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
        TIMESTAMP_DIFF(dropoff_datetime, pickup_datetime, SECOND) as trip_duration
    from {{ ref('dim_fhv_trips') }}
),

p90_trips as (
    select 
    pickup_year,
    pickup_month,
    PUlocationid,
    --pickup_borough,
    --pickup_zone,
    DOlocationid,
    --dropoff_borough,
    --dropoff_zone,
    APPROX_QUANTILES(trip_duration, 100)[OFFSET(90)] AS p90_duration  -- 90th percentile
from fhv_trips_data
group by pickup_year,
    pickup_month,
    PUlocationid,
    DOlocationid
order by pickup_year, pickup_month
)

select fhv_trips_data.* ,
p90_trips.p90_duration
from fhv_trips_data
join p90_trips 
ON fhv_trips_data.pickup_year = p90_trips.pickup_year
AND fhv_trips_data.pickup_month = p90_trips.pickup_month
AND fhv_trips_data.PUlocationid = p90_trips.PUlocationid
AND fhv_trips_data.DOlocationid = p90_trips.DOlocationid
