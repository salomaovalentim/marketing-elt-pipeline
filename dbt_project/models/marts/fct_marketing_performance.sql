with spend as (
    select
        campaign_id,
        spend_date as event_date,
        sum(amount_spent) as total_spend,
        sum(impressions) as total_impressions,
        sum(clicks) as total_clicks
    from {{ ref('stg_ad_spend') }}
    group by 1, 2
),

events as (
    select
        campaign_id,
        cast(event_timestamp as date) as event_date,
        count(case when event_type = 'conversão/compra' then 1 end) as total_conversions,
        sum(conversion_value) as total_revenue
    from {{ ref('stg_tracking_events') }}
    group by 1, 2
),

joined as (
    select
        coalesce(s.campaign_id, e.campaign_id) as campaign_id,
        coalesce(s.event_date, e.event_date) as event_date,
        coalesce(s.total_spend, 0.00) as total_spend,
        coalesce(s.total_impressions, 0) as total_impressions,
        coalesce(s.total_clicks, 0) as total_clicks,
        coalesce(e.total_conversions, 0) as total_conversions,
        coalesce(e.total_revenue, 0.00) as total_revenue
    from spend s
    full outer join events e
        on s.campaign_id = e.campaign_id
        and s.event_date = e.event_date
),

metrics as (
    select
        campaign_id,
        event_date,
        total_spend,
        total_impressions,
        total_clicks,
        total_conversions,
        total_revenue,
        round(
            (total_clicks::numeric / nullif(total_impressions, 0)) * 100, 
            2
        ) as ctr_percentage,
        round(
            total_spend / nullif(total_clicks, 0), 
            2
        ) as cpc,
        round(
            total_spend / nullif(total_conversions, 0), 
            2
        ) as cpa,
        round(
            total_revenue / nullif(total_spend, 0), 
            2
        ) as roas,
        round(
            ((total_revenue - total_spend) / nullif(total_spend, 0)) * 100, 
            2
        ) as roi_percentage
    from joined
)

select * from metrics