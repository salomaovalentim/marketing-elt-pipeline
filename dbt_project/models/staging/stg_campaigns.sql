with source as (
    select * from {{ source('raw_data', 'raw_campaigns') }}
),

renamed as (
    select
        cast(campaign_id as text) as campaign_id,
        trim(campaign_name) as campaign_name,
        lower(trim(objective)) as objective,
        lower(trim(media_type)) as media_type,
        cast(start_date as date) as start_date,
        cast(end_date as date) as end_date,
        lower(trim(status)) as status
    from source
)

select * from renamed