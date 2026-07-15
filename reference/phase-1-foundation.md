# Corax Arcana — Phase 1: Product Foundation

The minimum that gets someone to create an account and come back the next day. Launchable MVP. 18 tasks.

---

## Group A — Infrastructure and authentication (do first, everything depends on it)

### 01 - Project and repository setup
*Easy - Platform*
Monorepo, basic CI/CD, dev/staging/prod environments, local Docker Compose.
- Create GitHub repo with folder structure
- Configure Docker Compose (backend, database, redis)
- Set up CI with GitHub Actions (lint + tests)
- Environment variables per environment (dev/staging/prod)

### 02 - Database and initial data model
*Easy - Platform*
PostgreSQL schema with users, cards, collections, decks tables.
- users table (id, email, name, plan, created_at)
- cards table (reference to Scryfall — don't duplicate data)
- user_cards table (user_id, card_id, qty, condition, foil, edition)
- decks + deck_cards tables

### 03 - Authentication with Google and email
*Easy - Platform*
Social login (Google OAuth2) + email/password. JWT with refresh token.
- Google OAuth2
- Email + password with confirmation
- JWT access token (15min) + refresh token (30 days)
- Password reset route

### 04 - Freemium model — limits and plans
*Easy - Platform*
Define what's free and what's Pro. Implement plan-verification middleware.
- Free tier: up to 500 cards, 5 decks, no alerts
- Pro tier: unlimited + all advanced features
- checkPlan() middleware for restricted routes
- Clear pricing page

---

## Group B — Scryfall integration (card database)

### 05 - Scryfall API integration
*Easy - Collection*
Search cards by name, set, filters. Local cache to avoid depending on external latency.
- GET /cards/search?q= endpoint via Scryfall
- Redis cache with 24h TTL per card
- Daily sync of new cards (cron job)
- Handle Scryfall rate limits (max 10 req/s)

### 06 - Advanced card search
*Easy - Collection*
Search interface with filters: color, type, CMC, rarity, set, legal format.
- Color filters (WUBRG + colorless + multicolor)
- Type filter (Creature, Instant, Sorcery...)
- Filter by set and block
- Filter by format legality

### 07 - Price integration (TCGPlayer / Cardmarket / Ligamagic)
*Medium - Collection*
Pull updated prices. For BR, prioritize Ligamagic or CardMarket EUR.
- Scryfall already returns USD and EUR prices — use as base
- Daily job to update prices in the database
- Display price in BRL using dollar/euro exchange rate
- Price history: store daily snapshot

---

## Group C — Personal collection management

### 08 - Manually add a card to the collection
*Easy - Collection*
Interface to search for a card, choose edition, quantity, condition, and foil.
- Search card by name (autocomplete)
- Select edition/set
- Set quantity (regular + foil separately)
- Set condition: NM / LP / MP / HP / DMG

### 09 - Complete collection inventory
*Easy - Collection*
Paginated list of all the user's cards with filters, search, and sorting.
- Listing with card thumbnail
- Filter by color, type, set, condition
- Sort by name, value, quantity
- Compact mode (list) and expanded mode (image grid)

### 10 - Collection value dashboard
*Easy - Collection*
Current total value, day's variation, top 10 most valuable cards.
- Card: total collection value in BRL
- Card: last 24h variation (green/red)
- List: top 10 most valuable cards
- Chart: total value evolution over the last 30 days

### 11 - Collection import via CSV / Moxfield / MTGO
*Medium - Collection*
Import collection from another platform to avoid starting from zero.
- Generic CSV parser (name, qty, set, condition)
- Moxfield format import (JSON export)
- MTGO decklist import (.txt)
- Import report: X cards added, Y errors

### 12 - Card wishlist
*Easy - Collection*
List of cards the user wants to buy, with target price and priority.
- Add card with target price and priority
- View current price vs. target price
- Total cost to complete the wishlist
- "Already have it" flag when the card enters the collection

---

## Group D — Deck builder

### 13 - Create and edit decks
*Medium - Deck Builder*
Deck builder interface with main deck, sideboard, maybeboard, and commander.
- Create deck with name, format, and description
- Add cards via search (autocomplete)
- Zones: main (60/100), sideboard (15), maybeboard
- Remove and adjust quantities

### 14 - Automatic legality validation
*Medium - Deck Builder*
Check if the deck follows the selected format's rules (ban list, copy limit).
- Validate the 4-copy limit (except basic lands)
- Validate ban list per format (updated via Scryfall)
- Highlight illegal cards in red
- Show invalid deck warning before saving

### 15 - Mana curve analysis
*Easy - Deck Builder*
Bar chart with CMC distribution and basic mana base analysis.
- Bar chart: number of cards per CMC
- Breakdown by mana color (pips)
- Suggested number of lands per color
- Alert if the curve looks too heavy or too light

### 16 - Deck cost — what you have vs. what's missing
*Easy - Deck Builder*
See which cards in the deck you already own in your collection and the cost of the missing ones.
- "Have X" badge for each card in the deck
- List of missing cards with unit price
- Total cost to complete the deck
- "Add missing cards to wishlist" button

### 17 - Share deck via public link
*Easy - Deck Builder*
Generate a public deck URL viewable without needing an account.
- /deck/:id/public route without authentication
- Display formatted decklist with images
- "Clone this deck" button for logged-in users
- Toggle: public or private deck

---

## Group E — Basic finances

### 18 - Magic spending log
*Easy - Finances*
Log purchases of cards, accessories, and tournament entry fees with category and date.
- Form: date, amount, category, description
- Categories: single card, pack/booster, accessory, tournament, other
- Spending list with filter by period and category
- Total spent this month / this year
