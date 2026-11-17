# Règles de qualité — fichier de janvier 2024

## Principe
Trois statuts : accepté, signalé (conservé avec un drapeau), rejeté
(écarté vers la table des rejets avec son motif). Un rejet l'emporte
sur un signalement. On rejette seulement ce qui est impossible.

## Règles
- R1 Année du départ hors 2023-2024 : rejet (5 lignes).
- R2 Départ hors du mois mais plausible : signalée (13 lignes).
  Risque de doublon avec les fichiers voisins, à vérifier au chargement incrémental.
- R3 Durée négative, ou nulle avec distance > 0 : rejet (112 lignes).
- R4 Vitesse > 100 mph : rejet (1 024). De 60 à 100 mph : signalée (265).
- R5 Distance 0 ou durée 0 : même zone, acceptée ; zones différentes
  ou durée 0, signalée.
- R6 total_amount < 0 : types 3 ou 4 acceptés, autres signalés.
  fare_amount < 0 seul : signalé.
- R7 total_amount = 0 : types 3 ou 4 acceptés, autres signalés.
- R8 Colonnes vides avec payment_type = 0 (Flex Fare) : acceptées.

## Limites connues
- Seuils de vitesse fondés sur la distribution de janvier 2024, à revalider
  avec février et mars.
- 2 064 lignes avec fare_amount < 0 et total_amount >= 0 non analysées.