import logging
from pathlib import Path

from connexion import connecter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger("snowflake").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

RACINE = Path(__file__).resolve().parent.parent
STAGE = "@NYC_TAXI.BRONZE.STG_RAW"
TABLE = "NYC_TAXI.BRONZE.TAXI_ZONES"
NOM_FICHIER = "taxi_zone_lookup.csv"


def charger_zones() -> None:
    """Envoie le référentiel des zones au stage, puis le charge dans Bronze."""
    chemin = RACINE / "data" / "raw" / NOM_FICHIER
    if not chemin.exists():
        raise FileNotFoundError(chemin)

    with connecter() as conn:
        cur = conn.cursor()

        log.info("PUT %s", NOM_FICHIER)
        cur.execute(f"PUT 'file://{chemin.as_posix()}' {STAGE} AUTO_COMPRESS=FALSE")
        log.info("Résultat du PUT : %s", cur.fetchall())

        log.info("COPY INTO %s", TABLE)
        cur.execute(f"""
            COPY INTO {TABLE}
            FROM {STAGE}
            FILES = ('{NOM_FICHIER}')
            FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"')
        """)
        log.info("Résultat du COPY : %s", cur.fetchall())

        cur.execute(f"SELECT COUNT(*) FROM {TABLE}")
        log.info("Lignes en Bronze dans %s : %s", TABLE, cur.fetchone()[0])


if __name__ == "__main__":
    charger_zones()