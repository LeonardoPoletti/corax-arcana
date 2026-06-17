{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ref('stg_scryfall__cards')}}
),

deduped AS (
    SELECT
        *,
        ROW_NUMBER() OVER(
            PARTITION BY card_id
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