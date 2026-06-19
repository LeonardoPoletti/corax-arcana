{{ config(materialized='table') }}

WITH source AS(
    SELECT * FROM {{ ref('fct_card_prices')}}
),

final AS (
    SELECT
        set_code,
        set_name,
        rarity,

        -- How many unique cards exist in this set + rarity combination
        COUNT(DISTINCT card_id) AS card_count,

        -- How many of those cards actually have a price
        COUNT(price_usd) AS cards_priced_usd,
        COUNT(price_eur) AS cards_priced_eur,

        -- USD price stats
        ROUND(AVG(price_usd), 4) AS avg_price_usd,
        ROUND(MIN(price_usd), 4) AS min_price_usd,
        ROUND(MAX(price_usd), 4) AS max_price_usd,
        ROUND(SUM(price_usd), 4) AS total_value_usd,

        -- EUR price stats
        ROUND(AVG(price_eur), 4) AS avg_price_eur,
        ROUND(MIN(price_eur), 4) AS min_price_eur,
        ROUND(MAX(price_eur), 4) AS max_price_eur,
        ROUND(SUM(price_eur), 4) AS total_value_eur,

        -- When this data was last loaded from Scryfall
        MAX(price_date) AS last_updated

    FROM source
    GROUP BY set_code, set_name, rarity
)

SELECT * FROM final