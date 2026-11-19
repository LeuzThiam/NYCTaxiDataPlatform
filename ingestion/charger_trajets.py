import logging
import sys
from pathlib import Path

from connexion import connecter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

RACINE = Path(__file__).resolve().parent.parent
STAGE = "@NYC_TAXI.BRONZE.STG_RAW"
TABLE = "NYC_TAXI.BRONZE.YELLOW_TRIPS"


def charger_mois(mois: str) -> None:
    """Envoie le fichier Parquet d'un mois au stage, puis le charge dans Bronze."""
    nom_fichier = f"yellow_tripdata_{mois}.parquet"
    chemin = RACINE / "data" / "raw" / nom_fichier
    if not chemin.exists():
        raise FileNotFoundError(chemin)

    with connecter() as conn:
        cur = conn.cursor()

        log.info("PUT %s", nom_fichier)
        cur.execute(f"PUT 'file://{chemin.as_posix()}' {STAGE} AUTO_COMPRESS=FALSE")
        log.info("Résultat du PUT : %s", cur.fetchall())

        log.info("COPY INTO %s", TABLE)
        cur.execute(f"""
            COPY INTO {TABLE}
            FROM {STAGE}
            FILES = ('{nom_fichier}')
            FILE_FORMAT = (TYPE = 'PARQUET' USE_VECTORIZED_SCANNER = TRUE)
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
            INCLUDE_METADATA = (
                SOURCE_FILE = METADATA$FILENAME,
                SOURCE_ROW_NUMBER = METADATA$FILE_ROW_NUMBER
            )
        """)
        log.info("Résultat du COPY : %s", cur.fetchall())

        cur.execute(f"SELECT COUNT(*) FROM {TABLE} WHERE source_file = %s", (nom_fichier,))
        log.info("Lignes en Bronze pour %s : %s", nom_fichier, cur.fetchone()[0])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage : python ingestion/charger_trajets.py AAAA-MM")
    charger_mois(sys.argv[1])