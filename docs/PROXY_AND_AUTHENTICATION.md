# Proxy and Authentication Architecture

## Overview

Samsung DS mcp-atlassian uses **centralized proxy authentication**. Individual applications do NOT manage certificates.

```
┌─────────────────────────────────────────────────────┐
│ Your Code (mcp-atlassian)                           │
│  - Uses environment variables for proxy config      │
│  - NO client certificates                           │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ HTTP/HTTPS with proxy settings
                       │
┌──────────────────────▼──────────────────────────────┐
│ JFrog Artifactory (Corporate Proxy)                 │
│  - Handles all TLS/certificate management           │
│  - Validates downstream clients                     │
│  - Caches packages and credentials                  │
└──────────────────────┬──────────────────────────────┘
                       │
                       │ TLS with client certificates
                       │
┌──────────────────────▼──────────────────────────────┐
│ Jira / Confluence (Internal Servers)                │
└─────────────────────────────────────────────────────┘
```

## Environment Variables

Set these in `.env`:

```bash
# HTTP proxies (handled by JFrog)
HTTP_PROXY=http://proxy.samsungds.net:8080
HTTPS_PROXY=http://proxy.samsungds.net:8080
SOCKS_PROXY=socks5://proxy.samsungds.net:1080

# SSL verification (should be True)
SSL_VERIFY=true
```

**Do NOT set:**
- `CLIENT_CERT`
- `CLIENT_KEY`
- `CLIENT_KEY_PASSWORD`

These are no longer supported and will be ignored.

## Why This Matters

- ✅ **Developer Experience**: No certificate management burden
- ✅ **Security**: Keys managed centrally by IT
- ✅ **Compliance**: Enforces company security policies
- ⚠️ **Dependency**: Requires working proxy access

## Troubleshooting

**Q: Connection fails to Jira/Confluence?**
- A: Verify proxy URL and test: `curl -x [PROXY_URL] https://jira.samsungds.net/`

**Q: Package installation fails?**
- A: Check `uv.lock` is committed. Proxy handles caching.

---

See `INTERNAL_SETUP.md` for JFrog Artifactory dependency configuration.
