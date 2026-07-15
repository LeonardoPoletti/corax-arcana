# Corax Arcana — Phase 2: Differentiation and Retention

Features that turn a good product into a product people recommend. 22 tasks.

---

## Group A — Mobile and notifications (do first)

Without a PWA and notifications, everything after has reduced reach. The user needs an active communication channel before we activate alerts.

### 01 - PWA — Progressive Web App
*Medium - Platform*
Make the app installable on mobile (iOS and Android) without a store. Work offline for browsing already-loaded collections and decks.
- Create manifest.json with icons, splash screen, and app name
- Implement a Service Worker with a cache-first strategy for static assets
- Cache collection and deck pages for offline mode (Workbox)
- Show a native install banner on mobile after the 2nd visit
- Test installation on Chrome (Android) and Safari (iOS — limited but functional)

### 02 - Notification infrastructure (push + email)
*Medium - Platform*
Technical foundation for all platform alerts. Without this, the next groups are blocked.
- Integrate Firebase Cloud Messaging (FCM) for browser/PWA push
- Integrate a transactional email service (Resend or SendGrid)
- Create a user_notification_preferences table (type, channel: push/email/in-app, active)
- Create an async notification queue with BullMQ + Redis
- Create a preferences screen: enable/disable individually by type and channel
- Responsive email template with KyberCorax branding

### 03 - Camera card scanning
*Hard - Collection*
The most impressive feature for new users. Point your phone at the card and it's automatically added to the collection.
- Access camera via the MediaDevices API (Web) with a gently requested permission
- Capture a video frame and send it to the backend for analysis
- Backend: use Google Vision API or the Scryfall image endpoint to identify the card
- Return card with confidence %: ≥90% → confirm directly; 70–89% → show options; <70% → open manual search
- Batch scan mode: confirm one card and move straight to the next without leaving the screen
- Graceful fallback: if camera unavailable, show normal text search
- Depends on task 1 (PWA) to work well on mobile

---

## Group B — Alerts and market tracking

What makes the user open the app without needing external stimulus. When a notification arrives that a card has dropped in price, they come back.

### 04 - Daily price update job
*Medium - Collection*
Technical foundation for history and alerts. Persist daily price snapshots for cards tracked by users.
- Create a card_price_history table (card_id, date, price_usd, price_brl, source)
- Daily cron job (2am): fetch prices only for cards someone has in their collection or wishlist
- Convert USD → BRL using the day's exchange rate (Central Bank API or AwesomeAPI)
- Store only 1 snapshot per day per card to avoid bloating the database
- Execution log: how many cards updated, errors, execution time

### 05 - Price history per card
*Medium - Collection*
Price evolution chart for the last 30, 90, and 365 days for any card.
- GET /cards/:id/price-history?period=30d|90d|365d endpoint
- Interactive line chart on the frontend (Recharts or Chart.js)
- Mark relevant events on the timeline: ban, announced reprint, rotation
- Show: current price, min/max for the period, % variation
- Available on each card's detail page
- Depends on task 4 (accumulated history of at least 7 days to have a useful chart)

### 06 - Price variation alerts
*Medium - Collection*
Notify when a wishlist card drops below the target price — or when a collection card rises sharply.
- On the wishlist: "notify me when it reaches R$ X" field
- On the collection: "notify me if this card rises more than X%" toggle
- Post-price-update job: compare new prices with registered alerts
- Trigger notification (push or email, per preference) with card name + current price + variation
- Mark alert as "triggered" to avoid notifying every day while the price stays there
- Free limit: 5 active alerts. Pro: unlimited
- Depends on tasks 2, 4, and 5

### 07 - Set rotation reminders
*Medium - Gameplay*
Notify the user when cards from their Standard or Pioneer decks are about to rotate.
- Create a set_rotation_schedule table (set_code, format, rotation_date) — update manually each season
- Weekly job: cross-reference user decks with sets rotating in the next 90 days
- Staggered notification: 90 days before, 30 days before, rotation week
- "Rotation impact" screen: which cards leave each deck and substitute suggestions
- Only for decks tagged with Standard or Pioneer format
- Depends on task 2 (notifications) and the Phase 1 deck builder

---

## Group C — Advanced finances

The more hardcore player wants to know if they're "profiting" or "losing" with Magic. This group closes the financial loop started in Phase 1.

### 08 - Complete financial dashboard
*Medium - Finances*
Consolidated view of everything: how much you spent, what it's worth today, real ROI of the collection.
- Card: total spent (sum of all Phase 1 entries)
- Card: current collection value (real-time prices)
- Card: ROI = (current value − total spent) / total spent, in % and in R$
- Bar chart: monthly spending for the last 12 months
- Line chart: collection value over time (using price history)
- Breakdown by category: how much went to single cards, boosters, tournaments, accessories
- Depends on task 4 (price history) and the Phase 1 spending module

### 09 - Trade tracking
*Medium - Finances*
Log trades with fair value on both sides to keep real ROI in sight.
- Trade form: cards you gave + cards you received
- Value automatically calculated from each card's current prices
- Trade balance: did you gain or lose value? (e.g., "unfavorable trade of R$23")
- After confirming trade: move given cards out of the collection, add received ones
- Trade history with date, partner (free-text name), and balance
- Impact on ROI: was the trade good or bad for your collection long-term?

### 10 - Monthly budget with alerts
*Easy - Finances*
Monthly spending limit with real-time tracking and alerts before it's exceeded.
- Field on the finances screen: "my monthly Magic budget is R$ xxxx.xx"
- Progress bar: current spending / budget (green → yellow → red)
- Notification at 70%, 90%, and 100% of the budget
- Automatic reset at the start of each month
- History: how many months of the year you stayed within budget
- Depends on task 2 (notifications)

### 11 - ROI per card and per deck
*Medium - Finances*
See how much each card and each deck yielded financially — what appreciated, what depreciated.
- ROI per card: average acquisition price (recorded in entries) vs. current price
- ROI per deck: sum of card acquisition cost vs. current deck value
- Ranking: "your 10 most profitable cards" and "your 10 that depreciated the most"
- For cards without a registered acquisition price: use the average historical price from 1 year ago as an estimate (with a warning)
- Realized gain/loss: log when a card is sold or traded
- Depends on task 8 (dashboard) and task 9 (trades)

---

## Group D — Advanced deck builder

The Phase 1 deck builder is functional. Here it becomes the best in its category — with versioning, playtesting, and tools that Moxfield doesn't have.

### 12 - Import and export decklists as text
*Easy - Deck Builder*
Paste any decklist from any platform and export in standard formats. Eliminates migration friction.
- Text parser: recognize formats like "4 Lightning Bolt", "4x Lightning Bolt", "Lightning Bolt x4"
- Auto-detect sections: // Mainboard // Sideboard // Commander
- Typo correction suggestions for card names (fuzzy match)
- Export as: plain text, Arena format, MTGO format, JSON
- Support for cards named in PT-BR (e.g., "Relâmpago" → "Lightning Bolt")

### 13 - Deck tags and categories
*Easy - Deck Builder*
Organize the deck library with custom tags, status, and playstyle.
- Free tags: users create and apply their own tags (e.g., "FNM", "casual", "testing")
- Automatic system tags: detected format (Standard, EDH...) and style (aggro, control, combo, midrange)
- Deck status: draft, testing, finished, retired
- Filter and sort deck library by tag, status, format, last edited
- Visual color per tag for quick identification in the listing

### 14 - Deck version history
*Medium - Deck Builder*
Git-style deck versioning — save a snapshot, see what changed, restore a previous version.
- "Save version" button with a note field (e.g., "after Friday's FNM")
- deck_versions table (deck_id, snapshot JSON, note, created_at)
- History screen: list of versions with date and note
- Diff between versions: which cards were added and removed (shown in green/red)
- "Restore this version" button with confirmation
- Free limit: 5 versions per deck. Pro: unlimited

### 15 - Simulated playtester
*Hard - Deck Builder*
Virtually shuffle the deck, draw hands, and do draws to test consistency without needing physical cards.
- "Test deck" button on the deck builder screen
- Virtually shuffle the list and draw 7 cards (show images)
- London Mulligan: choose cards to bottom when taking a mulligan
- Additional draw card-by-card with a simple animation
- Flip battlefield cards (tapped/untapped indicator)
- Session-end statistic: % of hands with 2-4 lands across 20 simulations

### 16 - Sideboard assistant
*Hard - Deck Builder*
Sideboard suggestions based on the current meta of the deck's chosen format.
- Identify the deck's archetype: aggro, control, combo, midrange, tempo (by type and CMC)
- Fetch the top sideboards from the meta for that format (via MTGGoldfish or an in-house database)
- List the most commonly used hate cards for the format with usage frequency %
- Filter suggestions by cards the user already owns (prioritize what they have)
- Suggest 15 sideboard cards with justification: "vs. aggro", "vs. combo", etc.
- "Add to sideboard" button directly from the suggestion
- Depends on the meta analysis (task 17)

---

## Group E — Analysis and intelligence

Features that prove the platform "knows MTG" — it's not just an organizer, it's a strategic partner.

### 17 - Current meta analysis by format
*Hard - Analysis*
Which decks are dominating each format, with presence % and winrate. Updated weekly.
- Integrate with MTGGoldfish or MTGTOP8 via scraping (or a partner API if available)
- Weekly job: persist top 15 decks per format with name, presence %, winrate %
- Meta screen: filter by format, listing with archetype, presence, and winrate
- Archetype detail page: list of most-used cards in the archetype
- Highlight: "your deck [name] resembles [archetype X] from the meta"

### 18 - Budget-based deck suggestion
*Hard - Analysis*
User enters a budget and format, the platform builds a competitive deck that fits within it.
- Form: format, budget in BRL, preferred style (aggro, control, casual EDH...)
- Fetch meta decks close to the given budget
- Budget version: replace cards above budget with functional alternatives (curated substitute database)
- Calculate real cost accounting for cards the user already owns (automatic discount)
- "Create this deck" button → opens in the deck builder with all cards pre-added
- Depends on task 17 (meta) and Phase 1 real-time prices

---

## Group F — Content and education

Serves the beginner without alienating the hardcore player. Well-made content becomes organic traffic and reduces support load.

### 19 - Interactive beginner tutorial
*Medium - Content*
Guided onboarding for those who've never played Magic or just created their account. Reduces newcomer churn.
- Module 1 — how the game works: phases, card types, battlefield zones (with illustrations)
- Module 2 — how to register your collection: inventory demo + live card scan
- Module 3 — how to build your first deck: guided deck builder with inline tips
- Visible progress checklist on the dashboard: "you've completed 2 of 5 first steps"
- Contextual tooltips: appear the first time the user accesses each section (dismissible)
- Skip available at any time for experienced users

### 20 - Mana base calculator
*Easy - Content*
Tool to calculate the ideal number of lands per color, integrated into the deck builder.
- Inputs: deck's average CMC, % of cards per color, total non-lands
- Output: recommended total land count + split by color
- Base formula: Frank Karsten's rule (simplified hypergeometric regression)
- Dual land / fetch land suggestions for the mana base according to the format
- Inline version in the deck builder: "your mana base is X lands below recommended"

### 21 - Glossary of terms and mechanics
*Medium - Content*
Knowledge base of keywords, per-set mechanics, and competitive terms. Useful for beginners and as a quick reference for experienced players.
- Database of basic keywords (Trample, Deathtouch, Vigilance, Flash...)
- Per-set mechanics (Sagas, Adventures, Mutate, Daybound/Nightbound...)
- Competitive terms (APNAP, layers, priority, storm count, mana abilities...)
- Navigable search and index (A-Z + by set + by type)
- Integration: clicking a keyword in a card's text opens the glossary inline (tooltip)

### 22 - PT-BR and EN support (full i18n)
*Medium - Platform*
Internationalization of the entire interface. Essential for the Brazilian market and future expansion.
- Choose and set up an i18n framework: next-intl (Next.js) or i18next
- Extract all hardcoded frontend strings into translation files
- Translate the full interface: PT-BR and EN as base languages
- Automatically detect browser language on first visit
- Manual language toggle in user settings (persisted on the profile)
- Card names: display in the edition's language + EN name as a reference
