{{ config(materialized='table') }}

WITH cards AS (
    SELECT * FROM {{ ref('dim_card') }}
),

prices AS (
    SELECT
        card_id,
        ROUND(AVG(price_usd), 4) AS price_usd,
        ROUND(AVG(price_eur), 4) AS price_eur
    FROM {{ ref('fct_card_prices') }}
    GROUP BY card_id
),

-- Unpack legalities JSON: creates one row per card per format
format_rows AS (
    SELECT card_id, 'standard'  AS format_name, json_extract_string(legalities, '$.standard')  AS legality_status FROM cards WHERE legalities IS NOT NULL
    UNION ALL
    SELECT card_id, 'pioneer'   AS format_name, json_extract_string(legalities, '$.pioneer')   AS legality_status FROM cards WHERE legalities IS NOT NULL
    UNION ALL
    SELECT card_id, 'modern'    AS format_name, json_extract_string(legalities, '$.modern')    AS legality_status FROM cards WHERE legalities IS NOT NULL
    UNION ALL
    SELECT card_id, 'legacy'    AS format_name, json_extract_string(legalities, '$.legacy')    AS legality_status FROM cards WHERE legalities IS NOT NULL
    UNION ALL
    SELECT card_id, 'vintage'   AS format_name, json_extract_string(legalities, '$.vintage')   AS legality_status FROM cards WHERE legalities IS NOT NULL
    UNION ALL
    SELECT card_id, 'commander' AS format_name, json_extract_string(legalities, '$.commander') AS legality_status FROM cards WHERE legalities IS NOT NULL
    UNION ALL
    SELECT card_id, 'pauper'    AS format_name, json_extract_string(legalities, '$.pauper')    AS legality_status FROM cards WHERE legalities IS NOT NULL
),

legal_cards AS (
    SELECT
        f.format_name,
        c.rarity,
        p.price_usd,
        p.price_eur
    FROM format_rows f
    INNER JOIN cards c USING (card_id)
    LEFT JOIN prices p USING (card_id)
    WHERE f.legality_status = 'legal'
),

final AS (
    SELECT
        format_name,
        COUNT(*)                                         AS legal_card_count,
        COUNT(price_usd)                                 AS cards_priced,
        ROUND(AVG(price_usd), 4)                         AS avg_price_usd,
        ROUND(MAX(price_usd), 4)                         AS max_price_usd,
        COUNT(CASE WHEN rarity = 'mythic'   THEN 1 END)  AS mythic_count,
        COUNT(CASE WHEN rarity = 'rare'     THEN 1 END)  AS rare_count,
        COUNT(CASE WHEN rarity = 'uncommon' THEN 1 END)  AS uncommon_count,
        COUNT(CASE WHEN rarity = 'common'   THEN 1 END)  AS common_count
    FROM legal_cards
    GROUP BY format_name
    ORDER BY format_name
)

SELECT * FROM final