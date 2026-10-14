with customers as (
    select * from {{ ref('stg_crm_customers') }}
)

select
    customer_id,
    age,
    gender,
    state,
    city,
    signup_date,
    customer_segment
from customers