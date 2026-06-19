{{ config(materialized='table') }}

WITH source AS (
    SELECT * FROM {{ ref('fct_card_prices') }}
),

final AS (
    SELECT
        card_id,
        card_name,
        set_code,
        rarity,

        -- The Monday of each week (all days in the same week collapse to one row)
        DATE_TRUNC('week', price_date)     AS week_start,

        -- Weekly USD price statistics
        ROUND(AVG(price_usd), 4)           AS avg_price_usd,
        ROUND(MIN(price_usd), 4)           AS min_price_usd,
        ROUND(MAX(price_usd), 4)           AS max_price_usd,

        -- Weekly EUR price statistics
        ROUND(AVG(price_eur), 4)           AS avg_price_eur,
        ROUND(MIN(price_eur), 4)           AS min_price_eur,
        ROUND(MAX(price_eur), 4)           AS max_price_eur,

        -- How many days of price data we have for this card in this week
        COUNT(DISTINCT price_date)         AS days_of_data

    FROM source
    WHERE price_usd IS NOT NULL
    GROUP BY
        card_id,
        card_name,
        set_code,
        rarity,
        DATE_TRUNC('week', price_date)
)

SELECT * FROM final
ORDER BY card_name, week_start