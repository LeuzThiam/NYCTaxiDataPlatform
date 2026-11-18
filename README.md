# NYC Taxi Data Platform

Pipeline de données de bout en bout sur les courses de taxis jaunes de New York (NYC TLC, janvier à mars 2024) : ingestion en Python, stockage dans Snowflake, transformations avec dbt, modèle en étoile pour l'analyse.

> **Projet en cours.** Ce dépôt évolue module par module. La section « Avancement » indique ce qui est réellement terminé.

## Objectif

Construire une plateforme de données fiable et documentée, et répondre à trois questions métier :

1. Quelles zones génèrent le plus de revenus ?
2. Quels moments de la semaine sont les plus rentables ?
3. Quels moments de la journée sont les plus rentables ?

## Architecture

```
Fichiers Parquet (NYC TLC)
        |
        v   Python (PUT + COPY INTO)
  Snowflake - BRONZE   copie fidèle de la source + traçabilité
        |
        v   dbt
  Snowflake - SILVER   données nettoyées, validées, table des rejets
        |
        v   dbt
  Snowflake - GOLD     modèle en étoile (faits et dimensions)
```

Approche **ELT** : les données brutes sont chargées d'abord, puis transformées dans Snowflake. Tant que Bronze est conservé, on peut changer une règle de nettoyage et reconstruire Silver sans retélécharger les fichiers.

## Avancement

| Module | Contenu | État |
|---|---|---|
| 1 | Exploration des données et règles de qualité | Terminé |
| 2 | Ingestion Bronze (Python vers Snowflake) | En cours |
| 3 | Couche Silver (dbt) | À venir |
| 4 | Couche Gold, modèle en étoile (dbt) | À venir |
| 5 | Chargements incrémentaux et idempotence | À venir |
| 6 | Fiabilité : suivi des exécutions, reprise sur erreur | À venir |
| 7 | Tests et intégration continue | À venir |
| 8 | Consolidation et documentation finale | À venir |

Déjà en place : exploration documentée dans des notebooks, règles de qualité des données, conception de la couche Bronze, environnement Snowflake (entrepôt, base, schémas, stage, tables), compte de service avec rôle à privilèges minimaux et authentification par clé, module de connexion Python.

## Choix techniques

- **Snowflake** : entrepôt de taille minimale avec suspension automatique, rôle dédié au pipeline (moindre privilège), authentification du compte de service par paire de clés.
- **Python** : `pandas` et `pyarrow` pour l'exploration, `snowflake-connector-python` pour l'ingestion.
- **dbt** : transformations Silver et Gold (prévu).
- **Configuration** : variables d'environnement via un fichier `.env` local, jamais versionné.
- **Qualité des données** : on ne rejette que les lignes impossibles ; le reste est conservé avec un indicateur. Une ligne rejetée n'est pas supprimée, elle va dans une table de rejets avec sa raison. Voir `docs/regles_qualite.md`.
- **Git** : branches `main` (jalons stables), `develop` (intégration) et `feature/*`, `fix/*`, `docs/*` pour le travail.

## Structure du dépôt

```
docs/          règles de qualité, conception de la couche Bronze
exploration/   notebooks d'exploration (courses, zones)
ingestion/     code Python d'ingestion vers Snowflake
sql/           scripts Snowflake (entrepôt, stage, tables, rôles)
data/          fichiers sources (non versionnés)
```

## Prise en main

Prérequis : Python 3, un compte Snowflake et une paire de clés pour le compte de service.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Renseigne ensuite `.env` avec tes valeurs (compte, utilisateur, chemin de la clé privée). Ne versionne jamais ce fichier.

Les fichiers sources se téléchargent depuis le site de la NYC Taxi & Limousine Commission et se placent dans `data/raw/` :
`yellow_tripdata_2024-01.parquet` (et les mois suivants) et `taxi_zone_lookup.csv`.

Exécuter les scripts de `sql/` dans l'ordre (01 à 04) avec les rôles appropriés, puis :

```
python ingestion/connexion.py
```

## Source des données

NYC Taxi & Limousine Commission (TLC), données publiques des courses de taxis jaunes.
