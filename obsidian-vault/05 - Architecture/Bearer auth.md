---
title: Bearer auth
tags:
  - architecture
  - security
created: 2026-05-23
updated: 2026-05-23
---

# Bearer auth

> [!info] HTTP Authorization: Bearer scheme used by [[A2A Tier 2 - Server]]

## Config

```bash
A2A_API_KEYS=caller1=secret1,caller2=secret2
```

## Behavior

- If unset → server runs without auth (LOCAL DEV ONLY — never in production)
- If set → all `/a2a` requests must include `Authorization: Bearer <secret>` header
- Wrong/missing token → HTTP 401
- Per-caller rate limiting + task isolation use the caller name from this map

## Related

- [[A2A Tier 2 - Server]]
- [[Deploy targets]]

