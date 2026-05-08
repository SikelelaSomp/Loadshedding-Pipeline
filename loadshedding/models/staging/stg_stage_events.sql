with source as (
    select * from {{ source('raw', 'stage_events') }}
),

renamed as (
    select
        id,
        area_key,
        area_name,
        stage,
        stage_updated::timestamptz   as stage_updated_at,
        next_stages,
        retrieved_at::timestamptz    as retrieved_at,
        date(stage_updated)          as stage_date
    from source
)

select * from renamed