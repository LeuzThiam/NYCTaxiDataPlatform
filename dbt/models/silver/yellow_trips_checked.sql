with trips as (

    select * from {{ ref('stg_yellow_trips') }}

),

metrics as (

    select
        *,
        datediff('second', pickup_at, dropoff_at) as duration_seconds
    from trips

),

with_speed as (

    select
        *,
        case
            when duration_seconds > 0
            then trip_distance / (duration_seconds / 3600.0)
        end as speed_mph
    from metrics

)

select
    *,
    case
        when year(pickup_at) not in (2023, 2024)
            then 'R1_annee_hors_plage'
        when duration_seconds < 0
          or (duration_seconds = 0 and trip_distance > 0)
            then 'R3_duree_invalide'
        when speed_mph > 100
            then 'R4_vitesse_impossible'
    end as reject_reason
from with_speed