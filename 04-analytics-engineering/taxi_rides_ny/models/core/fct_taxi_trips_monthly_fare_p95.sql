{{ config(materialized='table') }}

with trips_data as (
    select * from {{ ref('fact_trips') }}
),

filtered_trips as (
    select 
    service_type,
    EXTRACT(year from pickup_datetime) as year,
    EXTRACT(month from pickup_datetime) as month,
    fare_amount
    from trips_data
    where fare_amount>0
    and trip_distance>0
    and payment_type_description in ('Cash', 'Credit card')
)

select
    service_type,
    year,
    month,
    APPROX_QUANTILES(fare_amount, 100)[OFFSET(50)] AS median_fare,  -- 50th percentile (median)
    APPROX_QUANTILES(fare_amount, 100)[OFFSET(90)] AS p90_fare,     -- 90th percentile
    APPROX_QUANTILES(fare_amount, 100)[OFFSET(95)] AS p95_fare,      -- 95th percentile
    APPROX_QUANTILES(fare_amount, 100)[OFFSET(97)] AS p97_fare      -- 97th percentile
FROM filtered_trips
GROUP BY service_type, year, month
ORDER BY service_type, year, month
