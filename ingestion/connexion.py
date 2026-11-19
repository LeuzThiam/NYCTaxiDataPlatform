import os
from pathlib import Path

import snowflake.connector
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

load_dotenv()

def lire_cle_privee() -> bytes:
    """Lit la clé privée chiffree (.p9) et la renvoie au format attendu par snowflake."""

    chemin = Path(os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"])
    passphrase = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE", "")

    cle = serialization.load_pem_private_key(
        chemin.read_bytes(),
        password=passphrase.encode() if passphrase else None,
    )
    return cle.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

def connecter():
    """Ouvrir une connexion snowflake avec l'authentification par clé privée."""
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        private_key=lire_cle_privee(),
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"]
    )

if __name__ == "__main__":
    with connecter() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE()"
        )
        print(cur.fetchone())