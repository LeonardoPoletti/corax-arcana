# Corax Arcana — Phase 3: Community and Viral Growth

Features that create network effect. The more users, the more valuable the product becomes. 20 tasks.

---

## Group A — Public profile and basic social features (do first)

Before any feed or marketplace, the user needs a public identity on the platform. Without a profile, there's no community.

### 01 - Public player profile
*Medium - Social*
Public page with decks, achievements, stats, and bio. This is the player's "identity" on the platform — the foundation for everything that comes after.
- Public route /player/:username, viewable without login
- Editable fields: photo, bio, city, favorite store, preferred formats, social links
- Public decks section with like and view counts
- Optional public stats: total cards, formats played, overall winrate
- Achievements and badges visible (comes from Group E)
- Privacy settings: each section can be public, friends-only, or private

### 02 - Social deck feed
*Medium - Community*
Timeline of decks published by all users. The platform's public showcase — what also appears to logged-out visitors.
- Chronological feed of decks marked public by any user
- Filters: by format (Standard, EDH, Pioneer...), by strategy (aggro, control...), by most recent / most liked
- Deck card in the feed: name, author, format, total cost, mini mana curve, like button
- Like / bookmark other users' decks (bookmark saves to your profile)
- Infinite-scroll pagination or "load more" button
- Feed for logged-out users: show featured public decks as a product showcase
- Depends on task 1 (public profile) — each deck in the feed links to the author's profile

### 03 - Deck comments
*Medium - Community*
Threaded comment system for giving constructive feedback on other users' decks.
- Nested comments: reply to a specific comment (max 2 levels)
- Inline card mentions: typing @CardName shows a card preview tooltip
- Minimal formatting: bold, italic, link
- Notification to the deck author when someone comments
- Notification to the commenter when someone replies
- Basic moderation: report button + automatic hiding after X reports
- Deck author can pin the best comment to the top
- Depends on task 2 (deck feed)

### 04 - Share deck as an image
*Medium - Social*
Generate a visually appealing image of the deck to post on Instagram, Twitter, WhatsApp, or Discord without needing to explain anything.
- Visual template: deck name, format, author, KyberCorax logo, grid of key card images
- Two versions: "summary" (commander/key cards + text list) and "full" (all cards in a grid)
- Server-side generation via Puppeteer or Satori (lighter) — return PNG
- Web Share API on mobile: "share" button opens the phone's native sheet
- Direct PNG download for desktop
- Canonical deck URL included in the image to drive traffic back to the platform

---

## Group B — EDH, matches, and tabletop tools

Commander is the most-played format in the world and the most socially connected. Those who play EDH play in groups — and groups create collective retention.

### 05 - EDH groups and pods
*Medium - Community*
Create Commander groups with members, table rules, session history, and each member's deck.
- Create group: name, description, table power level (1-10), custom rules, own ban list
- Invite members by link or email — accept/decline invite
- Each member associates which deck they're playing in the group (visible to everyone)
- Log session: date, which members played, which deck each used, who won
- Group stats: winrate per player, most-played decks, most winning commanders
- Simple group chat for scheduling matches
- Depends on task 1 (public profile) — each group member has their own profile

### 06 - Tournament and match journal
*Easy - Gameplay*
Log tournament results, casual matches, and opponents. Foundation for winrate statistics.
- Tournament entry: event name, date, format, entry fee in R$, store/location
- Tournament rounds: opponent, opposing deck (free-text name), result W/L/D
- Final placement and prize received (amount in R$ or description)
- Casual match entry: opponent, deck used, opposing deck, result, notes
- Free-text notes per match: "lost to burn on turn 3, need more removal"
- Prizes received are automatically logged as income in the financial module

### 07 - Winrate statistics per deck
*Easy - Gameplay*
Win percentage with each deck broken down by format, tournament vs. casual, and evolution over time.
- Overall winrate per deck: W / (W+L+D) in %
- Breakdown: tournament vs. casual vs. EDH (group session)
- Time evolution: monthly winrate chart (improving or declining over time?)
- Matchup summary: which archetypes you've won/lost against most (if logged)
- Minimum of 5 matches to display winrate (avoid misleading data)
- Comparison across all your decks: which has the best overall winrate
- Depends on task 6 (match journal) — the data comes from there

### 08 - Smart session life counter
*Easy - Gameplay*
Life counter for live sessions with history, poison tracking, energy, emblems, and commander damage.
- Configure session: 2, 3, or 4 players with name and photo (or avatar)
- Configurable starting life: 20 (duel), 40 (EDH), custom
- Track per player: life, poison counters (max 10), energy, emblems
- Commander damage: for each commander in the game, track damage dealt to each player separately
- History of life changes during the session (who dealt how much damage to whom)
- On session end: save result (who won) and offer to link it to the match journal
- Interface optimized for large screens (tablet) and small ones (phone in landscape)

### 09 - Round timer for tournaments
*Easy - Gameplay*
Configurable round timer with sound alerts. Simple but heavily used in casual tournaments organized by players themselves.
- Default timer: 50 minutes with free configuration (30, 40, 50, 60 min)
- Time extensions: +5 min button to add extra time
- Sound and visual alerts: 10 min left (yellow), 5 min (orange), time up (red + sound)
- Presentation mode: full-screen giant timer to project on the store's screen
- Round counter: round 1 of X with time history for each round
- Works offline (Phase 2 Service Worker already covers this)

---

## Group C — Marketplace and trades between users

The marketplace creates direct monetary value for the user — selling an expensive card on the platform is the most memorable experience possible. But it requires reputation and trust before money enters the picture.

### 10 - List cards for sale
*Medium - Marketplace*
List cards with photo, condition, and price for other platform users to see and buy.
- List directly from inventory: select an already-registered card and set a price (1 click)
- Listing fields: price in R$, condition, photos (max 3), notes, available quantity
- Public listing search: search by card name, filters by condition, price, and seller location
- Listing status: active, reserved (in negotiation), sold
- Automatic comparison: "this listing is X% below average market price"
- Free limit: 10 active listings. Pro: unlimited

### 11 - Internal chat for negotiations
*Medium - Marketplace*
Direct messages between users for handling trades, sales, and arrangements. Keeps the conversation inside the platform.
- Direct message triggered by an "I'm interested" button on a listing or profile
- Chat interface with conversation history (1:1, not a group)
- Push/email notification for new messages (via Phase 2 infrastructure)
- Share a card within the chat: select from collection and show with current price
- Read status: sent / seen
- Conversation archiving after 90 days of inactivity
- Report user directly from the chat screen
- Depends on task 10 (listings) — it's the marketplace's communication channel

### 12 - User reputation system
*Medium - Marketplace*
Rating and reviews after each completed transaction. Reputation is the user's most valuable asset on the marketplace.
- After a transaction is marked "completed": both sides receive a review request
- Rating: 1 to 5 stars + optional text field (max 300 characters)
- Public score on profile: average stars + number of rated transactions
- "Verified seller" badge for those with ≥20 transactions and average ≥4.5
- Review deadline: 15 days after completion, then it locks
- Reviews visible on the public profile — the seller can respond once per review
- Depends on tasks 10 and 11

### 13 - Automatic trade matching
*Hard - Marketplace*
The platform automatically cross-references wishlists with collections and notifies two users when there's a mutual trade match.
- Daily job: for each user, check if someone has cards from their wishlist AND wants cards from their collection
- Matching algorithm: A has X that B wants + B has Y that A needs → notify both
- Notification: "João has [card X] you want — and you have [card Y] he needs!"
- Trade proposal screen: list of cards from each side with automatically calculated value
- Balance indicator: fair trade / you gain the advantage / you're at a loss
- Accept proposal → opens chat between the two to work out details
- Depends on tasks 10, 11, and 12 — reputation must exist before automatic trades

---

## Group D — Content, reference, and extra tools

Features that add depth to the platform and drive organic traffic via SEO — public decks and the store map are indexable pages that attract players who don't even know the platform exists.

### 14 - Card detection by photo (refined version)
*Hard - Collection*
Evolve the Phase 2 scan into a more accurate and faster model, with support for PT-BR and Japanese cards.
- Evaluate the Phase 2 model's accuracy rate using real user data
- Train or fine-tune the model for alternate-art cards (borderless, showcase, extended)
- Support cards in other languages: JP, ES, PT — identify by artwork, not text
- Reduce response time: process the image on-device (TensorFlow.js) for common cards
- Bulk scan mode: continuous camera that keeps adding cards without pausing between each
- Incremental improvement over the Phase 2 scan — not built from scratch

### 15 - Art version comparator
*Medium - Collection*
View all editions and art versions of a card side by side to choose which to prefer or buy.
- List all printings of a card via Scryfall (/cards/:name/prints endpoint)
- Visual grid: card images with set, year, artist, and price for each version
- Filters: regular, foil, borderless, extended art, showcase, retro frame, serialized
- Sort by: price (low to high), date (oldest / newest), rarity
- Direct action: add a specific version to the collection or wishlist with one click

### 16 - New set spoiler feed
*Medium - Content*
News on new preview-set cards with meta impact analysis. Brings users back without needing marketing.
- Daily job: monitor Scryfall for cards from sets with a future preview_released_at
- Spoiler card: art, name, rules text, mana cost, rarity
- Team-curated estimated impact tag: "Standard threat", "EDH staple", "role-player", "bulk"
- "Add to wishlist" button directly from the spoiler (for when the card releases)
- Weekly spoiler notification for opted-in users
- Comments on the spoiler page (same infrastructure as task 3)
- Depends on task 3 (comments) for full engagement

### 17 - Nearby store and event map
*Hard - Gameplay*
Find Magic stores and FNM events, prereleases, and tournaments in the player's area. High value for casual players wanting to start playing in person.
- Interactive map via Google Maps API with pins for registered stores
- Store registration: self-registration by stores or user suggestion (manual review)
- Store profile: name, address, hours, formats played, social links, photos
- Events: FNM, prerelease, casual tournaments — registered by the store with date and format
- Search by city, ZIP code, or geolocation (with user permission)
- Store reviews from users with rating and comment (same reputation infrastructure)

### 18 - Card lore summaries
*Medium - Content*
For each card: a paragraph explaining who the character is and where they appear in the Multiverse's story. Attracts lore-focused players without needing to leave the platform.
- For main characters (Planeswalkers, legendaries): manually curated lore by the team
- For common cards: generated via LLM (Claude API) with a structured prompt + review
- Links to related cards: same saga, same plane, same character
- "Appears in" section on the card page: list of sets featuring the character
- "Card of the day" feature: random card with its lore on the homepage for logged-in users

---

## Group E — Gamification and recurring engagement

Achievements and the Discord bot are the two features with the highest organic virality potential — every shared badge and every Discord command is a free ad.

### 19 - Achievements and badges
*Medium - Social*
Achievement system for platform usage milestones. Small wins that build habit and healthy pride.
- Collection badges: 100 cards registered, 500, 1,000, 5,000, "legendary"
- Deck badges: first deck created, 10 decks, one deck in each format
- Community badges: first completed trade, 5-star rating, first comment
- Tournament badges: participated in a tournament, first top 8, champion
- Secret badges: discovered by performing unusual actions (easter eggs)
- Achievement-unlocked notification with animation (not annoying — only once)
- Displayed on the public profile with achievement date and option to feature favorites

### 20 - Discord bot — basic integration
*Hard - Social*
Bot for Magic Discord servers to look up prices, decks, and meta without leaving Discord. Free marketing on every server that installs it.
- Create a Discord application and register slash commands via the Discord Developer Portal
- /price [card name] → returns current price in R$ and USD with card thumbnail
- /deck [link or name] → shows deck summary (commander, cost, format)
- /meta [format] → top 5 meta decks with presence % (Phase 2 data)
- /spoiler → shows the most recent spoiler for the next set
- OAuth2: link Discord account with platform account for personalized features
- Bot installation page with instructions and invite link
- Depends on Phase 2's meta analysis (task 17) and spoiler feed (task 16)
