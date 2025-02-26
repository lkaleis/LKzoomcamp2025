{{
    config(
        materialized='view'
    )
}}

with fhv_tripdata as 
(
  select *
  from {{ source('staging','fhv_data') }}
  where dispatching_base_num is not null 
)

select * 
from fhv_tripdata


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}