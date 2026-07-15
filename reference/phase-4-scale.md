# Corax Arcana — Phase 4: Scale, Advanced AI, and Innovation

Ambitious features, some out of the box. Implement once the foundation is already solid. 18 tasks.

---

## Group A — Native mobile app (do first)

The Phase 2 PWA is good, but it has real limitations on iOS (camera, push, performance). A native app unlocks the full experience and signals product maturity to the market.

### 01 - iOS and Android app with React Native + Expo
*Very Hard - Platform*
Dedicated app with a high-performance native camera, real notifications, full offline mode, and platform-optimized UX.
- Project setup with Expo SDK — shared code between iOS and Android
- Native camera (expo-camera) replacing the Web API — much faster and more accurate card scanning
- Native push notifications: APNs (iOS) + FCM (Android) via Expo Notifications
- Full offline mode: local SQLite with automatic sync on reconnect (expo-sqlite + background fetch)
- Native navigation: tab bar, stack navigation, swipe gestures
- Deep linking: site links open directly in the app if installed
- App Store (Apple) and Google Play publication with review process
- CI/CD for automatic builds via EAS Build (Expo Application Services)

### 02 - Optimized batch scan in the native app
*Hard - Collection*
With a native camera, evolve the scan to process multiple cards in quick succession — ideal for cataloging large collections.
- Continuous camera mode: confirm a card → camera is already ready for the next
- Partial on-device recognition with TensorFlow Lite (most common cards without needing the network)
- Processing queue: take photos faster than the backend responds — process in batches
- Final review: summary screen with all scanned cards to confirm before saving
- Session stats: X cards scanned in Y minutes
- Depends on task 1 (native app) — doesn't make sense as a PWA

---

## Group B — Full marketplace with payments

Phase 3 created the marketplace with chat and reputation. Now real money enters — payment gateway, buyer protection, and integration with external platforms.

> Prerequisite: at least 500 active users and a reputation system with real history (Phase 3) before enabling payments.

### 03 - Payment gateway — Pagar.me or Stripe
*Very Hard - Marketplace*
Buying and selling cards within the platform with real money, automatic split, and protection for both parties.
- Integrate Pagar.me (BR focus: PIX, boleto, card) or Stripe with BRL support
- Payment split: buyer pays → platform retains fee (e.g., 8%) → seller receives the rest
- Escrow system: money held until buyer confirms receipt (7-day window)
- Dispute opening: buyer can contest within the window — team reviews
- Simplified KYC for sellers: CPF + bank details to receive payments
- Seller financial dashboard: available balance, pending, withdrawal history
- Compliance: issuing an invoice or electronic receipt for transactions above R$X

### 04 - Correios and Melhor Envio integration
*Hard - Marketplace*
Integration with Correios and Melhor Envio.
- Melhor Envio API integration: calculate Correios, JadLog, Loggi shipping by ZIP code and weight
- Automatic estimated weight: 1 sleeved card ≈ 5g, 60 cards ≈ 120g — reference table
- Buyer chooses shipping method before completing purchase
- Seller generates a paid shipping label directly from the app (deducted from balance)
- Integrated tracking: shipment status visible to buyer and seller in the transaction chat
- Automatic receipt confirmation when Correios delivery is detected
- Depends on task 3 (payment gateway)

### 05 - Automatic Mercado Livre publishing - out of the box
*Very Hard - Marketplace*
List a card on the platform and automatically publish it on ML at the same time. Manage all listings from one place.
- OAuth integration with Mercado Livre via the official API (MercadoLibre Developers)
- Category mapping: "Card Games → Magic: The Gathering → [set]"
- Bidirectional sync: sold on ML → remove from platform; sold on the platform → pause on ML
- Manage ML questions directly from the platform's internal chat
- Unified report: sales by channel (platform vs. ML vs. others)
- Depends on tasks 3 and 10 from Phase 3 (listings)

---

## Group C — Advanced AI (depends on accumulated data)

These features need real usage data to work well. Without match history, there are no matchup patterns. Without 1+ year of price history, there's no reliable appreciation model. Building too early wastes effort.

> Prerequisite: minimum 6 months of real usage data from Phases 1–3 before building the models in this section.

### 06 - AI hand analysis - out of the box
*Very Hard - Analysis & AI*
User sends a photo of their opening hand and receives an analysis: keep, mulligan, with strategic reasoning based on the deck.
- Recognize the 7 cards from the photo (evolving the scan — native app task 2)
- Cross-reference with the selected deck: what kind of hand is this within the deck's strategy?
- LLM analysis (Claude API): "you have 3 lands, 2 removal spells, and 2 threats — keepable hand for control"
- Clear output: KEEP / MULLIGAN / SITUATIONAL with a confidence level
- Bullet-point reasoning: "enough lands ✓", "no win condition before turn 5 ✗"
- History: save analyses to train a proprietary model in the future
- Depends on the refined scan (task 2) and the deck builder with archetype identification (Phase 2)

### 07 - Complete matchup analyzer
*Very Hard - Analysis & AI*
Historical statistics on how each archetype performs against others — and how your specific deck fares in the meta.
- Tournament results database: MTGO challenge results, mtgtop8 (scraping or partnership)
- Archetype identification model from card lists (similarity clustering)
- Matchup matrix: aggro vs. control vs. combo vs. midrange by format
- Deck page: "against Mono Red you have a 45% historical winrate"
- Automatically generated sideboard suggestions per matchup
- Incorporate match data logged by the platform's own users (Phase 3)
- Depends on Phase 3's match journal and Phase 2's meta analysis

### 08 - Ban prediction - out of the box
*Very Hard - Analysis & AI*
A model that analyzes presence, winrate, and trends of cards and estimates ban probability — alerts users who own those cards.
- Model features: meta presence %, winrate %, weekly growth rate, forum complaints
- Train the model using past ban history (2010–2024) as ground truth
- Risk score per card per format: low / medium / high / critical
- User alert: "your card [X] has a high ban risk in Modern — consider selling"
- Public page: "ban thermometer" — the 10 highest-risk cards in the current meta
- Clear disclaimer: this is data-based speculation, not an official prediction
- Depends on 1+ year of accumulated price and meta data on the platform

### 09 - Personal power ranking with player profile - out of the box
*Very Hard - Analysis & AI*
A system that learns the user's playstyle over time and makes increasingly personalized suggestions.
- Onboarding interface: swipe on cards (like / dislike / neutral) — 20 initial cards
- Inferred profile: aggressive / controlling / combo / thematic / casual / financial
- Continuously feed the profile: decks created, wishlist cards, logged matches
- Deck recommendations aligned with the profile: "based on your style, you'll like [archetype X]"
- Card purchase suggestions: "players with a profile similar to yours tend to have [card Y]"
- Allow reset and manual adjustment of the profile at any time
- Depends on 3+ months of usage history for the profile to be reliable

### 10 - Card appreciation projection - out of the box
*Very Hard - Finances*
Estimate future card value considering price history, reprint announcements, rotation, and meta popularity.
- Time series model (ARIMA or Prophet) trained on 1+ year of price history
- External factors as features: reprint announcement (decreases price), ban (decreases), rotation (decreases), synergy spoiler (increases)
- "Appreciation potential" score per card: pessimistic / neutral / optimistic
- Integrate into the financial dashboard: "your collection has +R$X potential over the next 6 months"
- Mandatory, visible disclaimer: this is not financial advice, it's speculative analysis
- Depends on 1+ year of accumulated price history — doesn't work with short data

---

## Group D — Advanced finance and compliance

Features that serve the serious player/collector who treats Magic as an investment — and needs documentation for it.

### 11 - Tax report for IRPF
*Hard - Finances*
Export a purchase and sale report for income tax filing — especially relevant for those selling above R$35k/month.
- Log the acquisition cost of each card (already done in spending entries)
- Calculate capital gain: sale price − acquisition cost per transaction
- Monthly report: total sales, total cost, gross profit, applicable rate
- Automatic alert: "you sold more than R$35k this month — you may need to issue a DARF"
- Export as formatted PDF + CSV compatible with the Receita Federal's IRPF program
- Disclaimer: consult an accountant. The platform organizes data, it doesn't provide tax advice
- Depends on the payment gateway (task 3) to have real sales data

### 12 - Collection insurance — insurer partnership - out of the box
*Very Hard - Finances*
For collections above R$5,000, offer insurance against theft, fire, and shipping damage via a B2B2C partnership.
- Commercial partnership with an insurer (B2B2C product — platform distributes, insurer underwrites)
- Value appraisal automatically generated by the platform based on market prices
- In-app contracting flow: insured value → coverage → monthly premium → contracting
- Digital insurance certificate generated and stored on the platform
- Coverage: theft, fire, shipping damage (for sales with shipping)
- Automatic renewal with updated insured value as the collection changes

---

## Group E — Advanced platform and community

Features that consolidate the platform as infrastructure for the MTG ecosystem in Brazil — and pave the way for international expansion.

### 13 - Complete draft simulator
*Hard - Gameplay*
Simulate drafts with random packs from any set, with pick notes, suggested archetype, and export to the deck builder.
- Generate 3 packs of 15 cards from a chosen set using correct rarity (1 rare, 3 uncommon, 11 common)
- Pick interface: show 15 cards, user picks 1, pack passes (simulated)
- Pick notes per card: integration with MTGDRAFTBOT or an in-house database (0–5 rating)
- Archetype suggestion throughout the draft: "you're heading into Dimir Control"
- Optional pick timer: 30, 60, or 90 seconds
- On finishing: export the drafted deck directly to the deck builder
- Draft history with pack 1's average rating, final archetype, winrate if later logged

### 14 - Platform-organized tournaments
*Hard - Community*
Create and manage tournaments with automatic Swiss pairing, live standings, and configurable prizing.
- Create tournament: name, format, date, location (online or physical), max players, entry fee
- Registration: through the platform with confirmation — waitlist if full
- Automatic Swiss pairing (standard DCI algorithm) per round
- Result reporting: each table reports W/L/D — cross-validation (both confirm)
- Live standings: table updated after each round with points and tiebreakers
- Cut to top 8 with a single-elimination bracket
- Configurable prizing: products, store credit, cash — record of prizes given
- Depends on Phase 3's tournament journal and public profiles

### 15 - Real-time deck collaboration - out of the box
*Very Hard - Social*
Build a deck with another person at the same time — like Google Docs for Magic. Ideal for building decks with your EDH partner or deck co-owner.
- WebSockets for real-time sync (Socket.io or Ably)
- Visible user cursors in the deck builder with name and color
- Action history: "João added 4x Lightning Bolt at 2:32 PM"
- Voting mode: each collaborator proposes cards, voting resolves ties
- Inline text chat during the collab session
- Permissions: deck owner can grant edit or view-only access

### 16 - Multiverse lore and history library
*Hard - Content*
Navigable wiki of MTG history — planes, characters, events, and timeline. High-value SEO for organic traffic.
- Plane database: Zendikar, Ravnica, Innistrad, Dominaria, Phyrexia, Eldraine... (profile + history)
- Character profiles: Planeswalkers + relevant secondary characters
- Navigable chronological timeline: order of Multiverse events
- Every card linked to the event/character in the lore wiki
- Community contribution: suggested edits with moderation (wiki-style)
- SEO: every character/plane page optimized for organic search

### 17 - Public API for developers
*Hard - Platform*
Public REST endpoints for integration with other tools — EDHREC, Archidekt, Chrome extensions, third-party apps.
- Authentication via an API key generated in the user panel (not OAuth, to keep it simple)
- Initial endpoints: GET /collection, GET /decks, GET /deck/:id, GET /card-price/:id
- Rate limiting by tier: Free (100 req/day), Pro (5,000 req/day), Partner (custom)
- Interactive documentation via Swagger/OpenAPI hosted at /developers
- Official SDK in Python and JavaScript (publish to PyPI and npm)
- Webhooks: notify an external URL when a card's price changes or a deck is updated

### 18 - Clans linked to physical stores
*Hard - Community*
Groups of players linked to physical stores with events, their own chat, and an optional loyalty program.
- Stores create a verified profile on the platform (continuation of Phase 3's store map)
- Users join their favorite store — appear as clan members
- Exclusive clan chat channel for members
- Store events appear in the feed and map only for members
- Optional points program: store defines the rules (e.g., 10pts per FNM attended)
- Clan ranking: stores with more active members get featured on the platform
- Depends on the store map (Phase 3, task 17) and groups (Phase 3, task 5)
