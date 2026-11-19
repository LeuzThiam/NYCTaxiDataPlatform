USE ROLE SYSADMIN;

-- Courses des taxis jaunes : copie fidèle du fichier source + traçabilité
CREATE TABLE IF NOT EXISTS NYC_TAXI.BRONZE.YELLOW_TRIPS (
    -- Colonnes du fichier source (noms et types d'origine)
    VendorID              INTEGER,
    tpep_pickup_datetime  TIMESTAMP_NTZ,
    tpep_dropoff_datetime TIMESTAMP_NTZ,
    passenger_count       INTEGER,
    trip_distance         FLOAT,
    RatecodeID            INTEGER,
    store_and_fwd_flag    VARCHAR,
    PULocationID          INTEGER,
    DOLocationID          INTEGER,
    payment_type          INTEGER,
    fare_amount           FLOAT,
    extra                 FLOAT,
    mta_tax               FLOAT,
    tip_amount            FLOAT,
    tolls_amount          FLOAT,
    improvement_surcharge FLOAT,
    total_amount          FLOAT,
    congestion_surcharge  FLOAT,
    Airport_fee           FLOAT,

    -- Colonnes de traçabilité
    source_file           VARCHAR,
    source_row_number     INTEGER,
    loaded_at             TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Référentiel des zones : le texte N/A est conservé tel quel
CREATE TABLE IF NOT EXISTS NYC_TAXI.BRONZE.TAXI_ZONES (
    LocationID   INTEGER,
    Borough      VARCHAR,
    Zone         VARCHAR,
    service_zone VARCHAR
);