{{ config(materialized='table') }}

with trips_data as (
    select * from {{ ref('fact_trips') }}
),

quarterly_rev AS (
    
    select 
    -- Revenue grouping 
    EXTRACT(YEAR from pickup_datetime) as year,
    EXTRACT(QUARTER from pickup_datetime) as quarter,
    FORMAT('%d-Q%d', EXTRACT(YEAR from pickup_datetime), EXTRACT(QUARTER from pickup_datetime)) as year_quarter,
    service_type, 

    -- Revenue calculation 
    sum(total_amount) as revenue_quarterly_total


    from trips_data
    group by year, quarter, year_quarter, service_type
)

select
*,
-- revenue for prev yearly quarter
lag(revenue_quarterly_total, 1) 
over 
(partition by quarter, service_type order by year) as prev_year_quarter_revenue,

-- % change
SAFE_DIVIDE(
        revenue_quarterly_total - LAG(revenue_quarterly_total, 1) OVER (
            PARTITION BY quarter, service_type ORDER BY year
        ), 
        LAG(revenue_quarterly_total, 1) OVER (
            PARTITION BY quarter, service_type ORDER BY year
        )
    ) * 100 AS yoy_qoq_percent_change
from quarterly_rev
order by service_type, year, quarter