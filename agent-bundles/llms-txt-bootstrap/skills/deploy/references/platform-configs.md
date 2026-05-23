# Extended Platform Configurations

*Per-platform deployment configurations beyond Nginx (which is in the base template). Load when the user's hosting platform is one of: Apache, Caddy, Vercel, Netlify, Cloudflare Workers/Pages, or a CDN-specific path.*

## Apache (httpd)

```apache
# In your main httpd.conf or a site-specific .conf file
<Files "llms.txt">
    ForceType "text/markdown; charset=utf-8"
    Header set X-Robots-Tag "noindex" always
    Header set Cache-Control "public, max-age=3600" always
    Header set Access-Control-Allow-Origin "*" always
</Files>

<Files "llms-full.txt">
    ForceType "text/markdown; charset=utf-8"
    Header set X-Robots-Tag "noindex" always
    Header set Cache-Control "public, max-age=3600" always
    SetOutputFilter DEFLATE
</Files>
```

Place llms.txt at the document root (`DocumentRoot/llms.txt`).

For Apache with mod_rewrite, also ensure no rewrites are interfering:
```apache
RewriteCond %{REQUEST_URI} !^/llms\.txt$
RewriteCond %{REQUEST_URI} !^/llms-full\.txt$
# ... other rewrite rules continue here
```

## Caddy

```caddy
example.com {
    @llms_txt path /llms.txt /llms-full.txt
    handle @llms_txt {
        header Content-Type "text/markdown; charset=utf-8"
        header X-Robots-Tag "noindex"
        header Cache-Control "public, max-age=3600"
        header Access-Control-Allow-Origin "*"
        file_server
    }

    # ... rest of your site config
}
```

Caddy auto-handles HTTPS via Let's Encrypt — `example.com` block above automatically provisions certs.

## Vercel

In `vercel.json` at your project root:

```json
{
  "headers": [
    {
      "source": "/llms.txt",
      "headers": [
        { "key": "Content-Type", "value": "text/markdown; charset=utf-8" },
        { "key": "X-Robots-Tag", "value": "noindex" },
        { "key": "Cache-Control", "value": "public, max-age=3600" },
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    },
    {
      "source": "/llms-full.txt",
      "headers": [
        { "key": "Content-Type", "value": "text/markdown; charset=utf-8" },
        { "key": "X-Robots-Tag", "value": "noindex" },
        { "key": "Cache-Control", "value": "public, max-age=3600" }
      ]
    }
  ]
}
```

Place the actual file at `public/llms.txt` (Next.js / static sites) or `static/llms.txt` (depending on framework).

For Next.js, you can also generate dynamically via a route handler:

```javascript
// app/llms.txt/route.js (Next.js 14+ app router)
export async function GET() {
  const content = await generateLlmsTxt(); // your generation logic
  return new Response(content, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'X-Robots-Tag': 'noindex',
      'Cache-Control': 'public, max-age=3600'
    }
  });
}
```

## Netlify

In `netlify.toml` at project root:

```toml
[[headers]]
  for = "/llms.txt"
  [headers.values]
    Content-Type = "text/markdown; charset=utf-8"
    X-Robots-Tag = "noindex"
    Cache-Control = "public, max-age=3600"
    Access-Control-Allow-Origin = "*"

[[headers]]
  for = "/llms-full.txt"
  [headers.values]
    Content-Type = "text/markdown; charset=utf-8"
    X-Robots-Tag = "noindex"
    Cache-Control = "public, max-age=3600"
```

For dynamic generation via Netlify Functions:

```javascript
// netlify/functions/llms-txt.js
export const config = { path: "/llms.txt" };

export default async () => {
  const content = await generateLlmsTxt();
  return new Response(content, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'X-Robots-Tag': 'noindex',
      'Cache-Control': 'public, max-age=3600'
    }
  });
};
```

## Cloudflare Workers / Pages

Workers script (static or dynamic):

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/llms.txt') {
      // Static: fetch from KV or R2
      const content = await env.LLMS_KV.get('llms.txt');

      return new Response(content, {
        headers: {
          'Content-Type': 'text/markdown; charset=utf-8',
          'X-Robots-Tag': 'noindex',
          'Cache-Control': 'public, max-age=3600',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    return new Response('Not Found', { status: 404 });
  }
};
```

For Cloudflare Pages with `_headers` file:

```
/llms.txt
  Content-Type: text/markdown; charset=utf-8
  X-Robots-Tag: noindex
  Cache-Control: public, max-age=3600
  Access-Control-Allow-Origin: *

/llms-full.txt
  Content-Type: text/markdown; charset=utf-8
  X-Robots-Tag: noindex
  Cache-Control: public, max-age=3600
```

## AWS CloudFront + S3

If serving from S3 with CloudFront in front:

**S3 object metadata** (set when uploading):
```bash
aws s3 cp llms.txt s3://your-bucket/llms.txt \
  --content-type "text/markdown; charset=utf-8" \
  --cache-control "public, max-age=3600" \
  --metadata-directive REPLACE
```

**CloudFront response-headers policy** (for `X-Robots-Tag`):
- Create a custom response headers policy in CloudFront
- Add `X-Robots-Tag: noindex` as a custom header
- Add to your distribution's behavior for `/llms.txt` path pattern

## Express / Node.js

```javascript
import express from 'express';
const app = express();

app.get('/llms.txt', (req, res) => {
  res.set({
    'Content-Type': 'text/markdown; charset=utf-8',
    'X-Robots-Tag': 'noindex',
    'Cache-Control': 'public, max-age=3600',
    'Access-Control-Allow-Origin': '*'
  });
  res.sendFile('llms.txt', { root: 'public/' });
});

app.get('/llms-full.txt', (req, res) => {
  res.set({
    'Content-Type': 'text/markdown; charset=utf-8',
    'X-Robots-Tag': 'noindex',
    'Cache-Control': 'public, max-age=3600'
  });
  res.sendFile('llms-full.txt', { root: 'public/' });
});
```

## Django / Python web frameworks

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('llms.txt', views.llms_txt, name='llms_txt'),
    path('llms-full.txt', views.llms_full_txt, name='llms_full_txt'),
]

# views.py
from django.http import FileResponse
from django.conf import settings
import os

def llms_txt(request):
    path = os.path.join(settings.BASE_DIR, 'static', 'llms.txt')
    response = FileResponse(open(path, 'rb'), content_type='text/markdown; charset=utf-8')
    response['X-Robots-Tag'] = 'noindex'
    response['Cache-Control'] = 'public, max-age=3600'
    return response
```

## CDN purge commands

### Cloudflare

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"files":["https://example.com/llms.txt","https://example.com/llms-full.txt"]}'
```

### Fastly

```bash
curl -X POST "https://api.fastly.com/service/$FASTLY_SERVICE_ID/purge/llms.txt" \
    -H "Fastly-Key: $FASTLY_API_KEY" \
    -H "Accept: application/json"
```

### AWS CloudFront

```bash
aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_DIST_ID \
    --paths "/llms.txt" "/llms-full.txt"
```

### Akamai

```bash
# Via Akamai CLI
akamai purge invalidate \
    https://example.com/llms.txt \
    https://example.com/llms-full.txt
```

## Cross-references

- `../SKILL.md` — main deployment flow
- `../../../templates/nginx-config.conf` — Nginx canonical config
- `../../../templates/validate.sh` — CI validation
- `ci-platforms.md` — CI/CD platform integrations
