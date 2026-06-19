{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ ref('stg_scryfall__cards') }}
),

final AS (
    SELECT
        -- Card identifiers
        card_id,
        oracle_id,
        card_name,
        set_code,
        set_name,
        rarity,
        collector_number,
        is_digital,
        is_foil,
        is_nonfoil,

        -- Prices unpacked from JSON string into real columns
        TRY_CAST(json_extract_string(prices, '$.usd')        AS DECIMAL(10,4)) AS price_usd,
        TRY_CAST(json_extract_string(prices, '$.usd_foil')   AS DECIMAL(10,4)) AS price_usd_foil,
        TRY_CAST(json_extract_string(prices, '$.usd_etched') AS DECIMAL(10,4)) AS price_usd_etched,
        TRY_CAST(json_extract_string(prices, '$.eur')        AS DECIMAL(10,4)) AS price_eur,
        TRY_CAST(json_extract_string(prices, '$.eur_foil')   AS DECIMAL(10,4)) AS price_eur_foil,
        TRY_CAST(json_extract_string(prices, '$.tix')        AS DECIMAL(10,4)) AS price_tix,

        -- The day this price snapshot was loaded from Scryfall
        CAST(_bronze_loaded_at AS DATE) AS price_date,

        -- Audit
        _bronze_loaded_at

    FROM source
    WHERE prices IS NOT NULL
)

SELECT * FROM final