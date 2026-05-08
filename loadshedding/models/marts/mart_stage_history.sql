with stage_events as (
    select * from {{ ref('stg_stage_events') }}
),

with_next_event as (
    select
        area_key,
        area_name,
        stage,
        stage_updated_at,
        stage_date,
        lead(stage_updated_at) over (
            partition by area_key
            order by stage_updated_at
        ) as next_stage_updated_at
    from stage_events
),

final as (
    select
        area_key,
        area_name,
        stage,
        stage_updated_at,
        next_stage_updated_at,
        stage_date,
        round(
            extract(epoch from (next_stage_updated_at - stage_updated_at)) / 3600
        , 2) as hours_at_stage
    from with_next_event
)

select * from final