with staging as (
    select * from {{ ref('stg_campaigns') }}
)

select
    campaign_id,
    campaign_name,
    channel,
    campaign_theme,
    objective,
    media_type,
    start_date,
    end_date,
    status
from staging