{{ config(materialized='view') }}

WITH source AS (
    SELECT *
    FROM read_parquet(
        '/home/leonardo/projects/corax-arcana/data/bronze/source=scryfall/entity=rulings/*.parquet'
    )
),

staged AS (
    SELECT
        -- Foreign key to cards
        oracle_id,

        -- Ruling information
        source AS ruling_source,
        comment AS ruling_text,

        -- Dates (cast from VARCHAR to DATE)
        try_cast(published_at AS DATE) AS published_at,

        -- Audit columns from Bronze
        loaded_at AS _bronze_loaded_at,
        _source,
        _file_name

    FROM source
)

SELECT * FROM staged