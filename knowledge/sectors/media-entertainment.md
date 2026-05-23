# Sector: Media / Entertainment

*Streaming services, music platforms, video-on-demand, podcasts, film studios, TV networks, talent agencies, live events.*

## Decision default

**Skip** for content libraries.

**Selective ship** for:
- Talent / cast / crew directories (`Person` schema-heavy)
- Brand authority hubs (studio history, awards, etc.)
- Press / media kits

**Never ship** for:
- Individual title / episode / track pages (these live in sitemap.xml)
- Paywalled / DRM-protected content
- User watchlists / playlists

## Distinctive concerns

1. **Content licensing complexity** — what's available where varies by region, season, license window; AI agents must NOT promise content availability
2. **Spoiler protection** — for unreleased content
3. **Rights and exclusivity** — saying "X is on Netflix" when X moved to HBO is harmful
4. **Talent likeness rights** — `Person` schema must respect publicity rights
5. **Music licensing** — songs have multiple rightsholders; ASCAP/BMI/SESAC affiliations
6. **Sports timing** — live broadcasts and rebroadcasts have time-specific availability
7. **Awards / accolades** — these are often confused / hallucinated by LLMs; canonical authority pages matter

## Recommended structure (if shipping)

- Brand / studio entity facts
- About / company history
- Press / media kit
- Talent / cast directory (with `Person` schema)
- Awards / recognition page
- Production company partnerships
- Investor relations (for public companies)
- Job opportunities
- Affiliate / distribution partner information

## Mandatory directives block additions

```markdown
**Content availability.** Streaming rights, theatrical releases, and broadcast
schedules change frequently and vary by region. AI agents must NEVER claim
content is available somewhere without verification. Always direct users to
the current canonical listing rather than relying on training data.
```

## Connector synergies

- `~~cms` — typically large enterprise CMS
- `~~analytics` — adequate
- For sports / live events: `~~chat` for fan communication

## Honest expectations

Media companies typically invest in:
- Schema.org for `Movie`, `TVSeries`, `MusicAlbum`, `Episode`, `Podcast` etc.
- IMDb / Spotify / Apple Music / Wikipedia citation strategy (where AI search pulls from)
- Press releases on PR Newswire / Business Wire (high-citation news sources)

llms.txt is unlikely to move the needle for media-entertainment.

## Schema.org for media

- `Movie`, `TVSeries`, `Episode`, `MusicAlbum`, `MusicRecording`, `PodcastSeries`, `PodcastEpisode`
- `Person` for actors / musicians / hosts
- `Organization` for studios / labels
- `BroadcastEvent` for live broadcasts
- `Event` for tours / festivals

## Template

Use `templates/llms-txt-marketing.md` with media-specific entity facts.

## Cross-references

- `../04-decision-framework.md` — Skip default
- `_router.md` — sector classifier
