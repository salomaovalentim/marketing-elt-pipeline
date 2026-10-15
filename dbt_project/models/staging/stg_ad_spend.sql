with source as (
    select * from {{ source('raw_data', 'raw_ad_spend') }}
)

select
    campaign_id,
    date as spend_date,
    amount_spent,
    total_impressions as impressions,
    total_clicks as clicks
from source