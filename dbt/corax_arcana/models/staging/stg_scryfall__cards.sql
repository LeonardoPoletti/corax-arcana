{{ config(materialized='view') }}

WITH source AS (
    SELECT *
    FROM read_parquet(
        '{{ env_var("DBT_BRONZE_PATH", "/home/leonardo/projects/corax-arcana/data/bronze") }}/source=scryfall/entity=cards/*.parquet'
    )
),

staged AS (
    SELECT

    -- Primay identifiers
    id AS card_id,
    oracle_id,
    name AS card_name,
    lang AS language,

    -- Card characteristics
    layout,
    mana_cost,
    cmc::DECIMAL(10,2) AS cmc,
    type_line,
    oracle_text,
    power,
    toughness,
    loyalty,
    colors,
    color_identity,
    keywords,

    -- Set information
    set_id,
    "set" AS set_code,
    set_name,
    set_type,
    rarity,
    collector_number,

    -- Legalities and prices (raw JSON - parsed in marts layer)
    legalities,
    prices,

    -- Rankings
    edhrec_rank,

    -- Boolean flags
    digital AS is_digital,
    reprint AS is_reprint,
    reserved AS is_reserved,
    foil AS is_foil,
    nonfoil AS is_nonfoil,
    full_art AS is_full_art,
    textless AS is_textless,
    oversized AS is_oversized,
    promo AS is_promo,
    booster AS is_booster,
    story_spotlight AS is_story_spotlight,

    -- Creative
    artist,
    flavor_text,
    watermark,

    -- Visual
    image_uris,
    image_status,
    border_color,
    frame,

    -- Dates (cast from VARCHAR to DATE)
    try_cast(released_at AS DATE) AS released_at,

    -- Audit columns from Bronze
    loaded_at AS _bronze_loaded_at,
    _source,
    _file_name

 FROM source
)

SELECT * FROM staged