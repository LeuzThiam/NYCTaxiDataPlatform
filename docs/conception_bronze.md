# Conception de la couche Bronze

## Rôle de Bronze

Bronze est la première couche de l'entrepôt. Elle conserve les données **telles qu'elles arrivent de la source**, sans correction, sans filtre et sans rejet. Les règles de qualité s'appliquent en Silver (voir `regles_qualite.md`).

Ce choix découle de l'approche ELT : on charge d'abord, on transforme ensuite dans la base. Tant que la donnée brute est conservée, on peut modifier une règle de nettoyage et reconstruire Silver sans retélécharger les fichiers.

## Sources

| Source | Format | Fréquence |
|---|---|---|
| `yellow_tripdata_AAAA-MM.parquet` (NYC TLC) | Parquet, typé | Un fichier par mois |
| `taxi_zone_lookup.csv` (NYC TLC) | CSV | Référentiel unique (265 zones) |

## Tables

### `bronze.yellow_trips`

- **Granularité :** une ligne = une ligne du fichier source.
- **Contenu :** les 19 colonnes du fichier, avec leur nom et leur type d'origine, plus 4 colonnes de traçabilité.
- **Structure :** une seule table pour tous les mois.

### `bronze.taxi_zones`

- **Granularité :** une ligne = une zone de taxi.
- **Contenu :** `LocationID`, `Borough`, `Zone`, `service_zone`.
- **Particularité :** le fichier est lu sans conversion automatique des valeurs vides (`keep_default_na=False`), pour conserver le texte `N/A` des zones 264 et 265. La traduction en valeurs explicites se fait en Silver.

## Colonnes de traçabilité

| Colonne | Type | Rôle |
|---|---|---|
| `source_file` | Texte | Nom du fichier d'origine. Permet de retrouver ou de remplacer un fichier précis. |
| `source_month` | Date | Premier jour du mois couvert par le fichier (par exemple `2024-01-01`). |
| `source_row_number` | Entier | Position de la ligne dans le fichier. |
| `loaded_at` | Horodatage | Date et heure du chargement. |

Ces colonnes ne modifient aucune donnée source : elles s'ajoutent à la fin de chaque ligne.

## Choix de conception et justifications

1. **Copie fidèle.** Aucune ligne n'est corrigée ni supprimée en Bronze. Les dates de 2002 ou les montants négatifs y sont conservés : on doit pouvoir expliquer ce qui est rejeté plus tard.
2. **Types d'origine conservés.** Un fichier Parquet est déjà typé. Charger tout en texte ajouterait des conversions inutiles. Les montants restent des flottants (`double`) ; la conversion en `DECIMAL` se fait en Silver.
3. **Noms de colonnes d'origine conservés**, y compris `Airport_fee`. La standardisation des noms se fait en Silver.
4. **Une seule table pour tous les mois.** Les fichiers mensuels ont le même schéma. Une table unique simplifie les requêtes, et `source_file` permet de remplacer un seul fichier sans toucher aux autres.
5. **Traçabilité minimale.** Les quatre colonnes ajoutées répondent à un besoin précis : retrouver la source (`source_file`, `source_month`), identifier une ligne source (`source_row_number`) et savoir quand elle est arrivée (`loaded_at`). On n'ajoute pas d'identifiant d'exécution pour l'instant : il n'aura de sens qu'avec la table de suivi des exécutions.

## Ce que Bronze ne fait pas

- Aucun nettoyage, aucune validation, aucun rejet.
- Aucun dédoublonnage : une ligne n'est pas une course, car les données ne fournissent pas d'identifiant fiable de course.
- Aucune jointure avec le référentiel des zones.

## Limites et points à revoir

- **Dérive de schéma.** On n'a examiné qu'un seul mois. Il faudra vérifier que février et mars ont le même schéma (noms, types) avant de les charger dans la même table.
- **Identité d'une ligne.** `source_file` et `source_row_number` identifient une ligne **source**, pas une course réelle. Cette distinction sera traitée dans la partie sur les chargements incrémentaux.
