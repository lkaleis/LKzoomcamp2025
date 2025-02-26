{{
    config(
        materialized='table'
    )
}}

with fhv_data_tripdata as (
    select *, 
        'fhv' as service_type
    from {{ ref('stg_fhv_trips') }}
),

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select 
    fhv_data_tripdata.*, 
    EXTRACT(year from pickup_datetime) as pickup_year,
    EXTRACT(month from pickup_datetime) as pickup_month,
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone

from fhv_data_tripdata
inner join dim_zones as pickup_zone
on fhv_data_tripdata.PUlocationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhv_data_tripdata.DOlocationid = dropoff_zone.locationid