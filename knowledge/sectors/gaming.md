# Sector: Gaming

*Game studios, publishers, platform holders (Steam, Epic, Xbox, PlayStation), esports orgs, gaming media, MMO communities, indie game sites.*

## Decision default

**Skip** for marketing pages.

**Selective ship** for:
- Game modding APIs (Steam Workshop, GameMaker, Roblox Creator, Unity asset store, etc.)
- Developer platform documentation (Steam SDK, PSN SDK, etc.)
- Wiki-style game encyclopedias (if you're a community wiki host)
- Esports tournament rules / format documentation

## Distinctive concerns

1. **Hype-driven release cycles** — game info changes drastically pre-release / launch / post-launch; freshness directives matter
2. **Modding ecosystems** — players want machine-readable game data; this is the legitimate "ship llms.txt" case
3. **Community wikis vs official sources** — for games with strong communities (Wowpedia, RuneScape Wiki, etc.), the wiki often has better/more current info than the publisher
4. **Region-specific releases** — games release by region with different dates and content
5. **Microtransaction / in-game economy info** — sensitive, fast-changing
6. **Age ratings** — ESRB / PEGI / CERO ratings vary by region; AI agents must respect these
7. **Storefront / patch note canonicality** — Steam News, PSN updates, Xbox blog all have different canonical content

## Recommended structure (for moddable game documentation)

- Game / engine entity facts (developer, publisher, release date, current version)
- API / SDK documentation
- Modding ecosystem entry point (workshop, mod portal)
- Tools and editor documentation
- Asset format specifications
- Multiplayer / networking protocol documentation
- Community resources (official forums, Discord, sub-reddit)
- Patch notes archive
- Localization / language support documentation

## Connector synergies

- `~~git` — heavy use; modding communities live on GitHub
- `~~docs-platform` — many use custom docs sites
- `~~chat` — Discord-heavy industry; community routing

## Honest expectations

- **For pure marketing**: same as marketing sector — null AI-citation lift.
- **For modding APIs**: this is essentially dev-docs — real benefit from developer/modder audience using AI coding assistants.
- **For game wikis**: tricky — Wikipedia/Reddit/Fandom typically dominate AI citations regardless of what you ship.

## Schema.org for gaming

- `VideoGame` for the game itself
- `Game` (broader) for non-video games
- `SoftwareApplication` with `applicationCategory: "GameApplication"`
- `Organization` for studio/publisher
- `Review` and `AggregateRating` for game reviews
- `Event` for tournaments

## Template

For modding APIs: `templates/llms-txt-dev-docs.md`
For marketing: `templates/llms-txt-marketing.md`

## Cross-references

- `../04-decision-framework.md` — Skip default
- `_router.md` — sector classifier
