with source as (
    select * from {{ source('raw_data', 'raw_campaigns') }}
),

renamed_and_cleaned as (
    select
        campaign_id::text as campaign_id,
        campaign_name as raw_campaign_name,

        -- Padronização do nome da campanha
        case 
            when lower(campaign_name) like '%black%friday%' or lower(campaign_name) like '%blackfriday%' 
                then 'Black Friday 2026'
            when lower(campaign_name) like '%google%search%' or lower(campaign_name) like '%pesquisa%' 
                then 'Google Search Institucional'
            when lower(campaign_name) like '%tiktok%' 
                then 'TikTok Brand Awareness'
            when lower(campaign_name) like '%rmkt%' or lower(campaign_name) like '%cart%' 
                then 'Remarketing Carrinho Meta'
            else initcap(replace(trim(campaign_name), '_', ' '))
        end as campaign_name,

        -- Identificação da plataforma / canal
        case
            when lower(campaign_name) like '%meta%' or lower(campaign_name) like '%facebook%' or lower(campaign_name) like '%instagram%'
                then 'Meta Ads'
            when lower(campaign_name) like '%google%' or lower(campaign_name) like '%search%'
                then 'Google Ads'
            when lower(campaign_name) like '%tiktok%' 
                then 'TikTok Ads'
            else 'Outros'
        end as channel,

        -- Categoria / Tema macro
        case 
            when lower(campaign_name) like '%black%friday%' or lower(campaign_name) like '%blackfriday%' 
                then 'Sazonal / Promocional'
            when lower(campaign_name) like '%rmkt%' or lower(campaign_name) like '%cart%' 
                then 'Fundo de Funil (Remarketing)'
            when lower(campaign_name) like '%brand%' or lower(campaign_name) like '%institucional%' 
                then 'Topo de Funil (Branding)'
            else 'Geral'
        end as campaign_theme,

        objective,
        media_type,
        start_date::date as start_date,
        end_date::date as end_date,
        status
    from source
)

select *
from renamed_and_cleaned