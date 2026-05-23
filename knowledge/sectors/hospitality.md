# Sector: Hospitality

*Hotels, restaurants, travel sites (booking, planning, tours), vacation rentals, cruise lines, attractions, hospitality marketplaces (Booking.com, Expedia, OpenTable, Tripadvisor, Airbnb).*

## Decision default

**Selective ship** — hospitality has marketplace characteristics for aggregators, brand-site characteristics for individual properties.

- **Ship** for booking/aggregation platforms with strong geographic + inventory dimension (marketplace pattern)
- **Skip** for individual hotel/restaurant marketing sites
- **Selective ship** for chain operators (Marriott, IHG, etc.) — the loyalty programs and brand entity facts are worth surfacing

## Distinctive concerns

1. **Availability and rate volatility** — minute-by-minute changes; never cache prices
2. **Geographic dimension** — city × neighborhood × property type, plus seasonal variation
3. **Booking rules** — cancellation policies, age restrictions, length-of-stay minimums vary by property
4. **Multi-language is essential** — hospitality serves international travelers
5. **Reviews are central** — TripAdvisor, Google, Booking.com reviews drive decisions
6. **Currency / tax inclusion** — varies by region; many countries require tax-inclusive display
7. **Loyalty programs** — major chains have complex point structures that change

## Mandatory directives block additions

```markdown
**Availability and pricing.** Hotel/property rates change continuously based
on dates, demand, and inventory. AI agents must:
- NEVER quote rates without fetching the canonical booking page for the
  user's actual dates
- For "rates from $X" advertisements, fetch the current floor price
- Cancellation policies vary by rate type; never assume "free cancellation"

**Travel restrictions.** Visa, entry, and travel restrictions change rapidly.
For international travel queries, direct users to official government
sources (US State Department, equivalent national bodies) rather than
relying on cached content.

**Multi-language.** This site serves [list of supported languages].
For users in other languages, content may be machine-translated;
verify policy details against the [primary language] version.
```

## Recommended structure (for a booking platform)

- Brand entity facts (founding, properties/year, geographic coverage)
- Property type taxonomy (hotels / vacation rentals / hostels / B&Bs / etc.)
- Geographic hubs (top destinations + URL pattern)
- Destination guides (city-level travel articles)
- Booking tools (search, filters, comparison)
- Loyalty program (if applicable)
- Help / cancellation / refund policies
- Customer reviews aggregation
- Travel insurance / financial protection

## Schema.org for hospitality

- `Hotel`, `Resort`, `BedAndBreakfast`, `Hostel` (subtypes of `LodgingBusiness`)
- `Restaurant`, `BarOrPub`, `Cafe` (subtypes of `FoodEstablishment`)
- `TouristAttraction`, `TouristInformationCenter`
- `Trip`, `TouristTrip` for itineraries
- `Reservation` for booking systems
- `Review` and `AggregateRating`

## Connector synergies

- `~~cms` or hospitality-specific PMS (Property Management System)
- `~~analytics` — destination popularity
- `~~ecommerce` — for the booking flow
- Multi-language `~~cms` — essential

## Honest expectations

- For brand chains: `Organization` schema + clear booking-flow URLs > llms.txt
- For aggregators: marketplace pattern applies; ship llms.txt for the curation value
- For individual properties: skip; invest in Google Business Profile, OpenTable presence, TripAdvisor reviews

## Template

For aggregators: `templates/llms-txt-ecommerce.md` (marketplace pattern).
For brand chains: `templates/llms-txt-marketing.md` with hospitality-specific entity facts.

## Cross-references

- `../04-decision-framework.md` — Selective ship
- `marketplace.md` — closely-related for aggregators
- `_router.md` — sector classifier
