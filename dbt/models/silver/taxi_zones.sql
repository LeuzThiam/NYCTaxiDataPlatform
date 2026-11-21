-- Référentiel des zones nettoyé :
-- noms de colonnes standardisés et texte 'N/A' remplacé par une valeur explicite

select
    LocationID as location_id,
    case when Borough = 'N/A' then 'Unknown' else Borough end as borough,
    case when Zone = 'N/A' then 'Unknown' else Zone end as zone,
    case when service_zone = 'N/A' then 'Unknown' else service_zone end as service_zone
from {{ source('bronze', 'taxi_zones') }}