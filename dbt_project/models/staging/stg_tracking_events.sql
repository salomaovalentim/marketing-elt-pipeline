with source as (
    select * from {{ source('raw_data', 'raw_tracking_events') }}
)

select
    event_id,
    campaign_id,
    customer_id,
    event_timestamp,
    event_type,
    conversion_value
from source