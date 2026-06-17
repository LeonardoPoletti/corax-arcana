{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ ref('stg_scryfall__rulings') }}
),

deduped AS (
    SELECT
        *,
        row_number() OVER (
            PARTITION BY oracle_id, ruling_text, published_at
            ORDER BY _bronze_loaded_at DESC
        ) AS row_num
    FROM source
),

final AS (
    SELECT * exclude (row_num)
    FROM deduped
    WHERE row_num = 1
)

SELECT * FROM final