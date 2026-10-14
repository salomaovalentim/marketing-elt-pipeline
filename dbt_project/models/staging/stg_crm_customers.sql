with source as (
    select * from {{ source('raw_data', 'raw_crm_customers') }}
),

renamed as (
    select
        cast(customer_id as text) as customer_id,
        cast(age as integer) as age,
        upper(trim(gender)) as gender,
        upper(trim(state)) as state,
        trim(city) as city,
        cast(signup_date as date) as signup_date,
        lower(trim(customer_segment)) as customer_segment
    from source
)

select * from renamed