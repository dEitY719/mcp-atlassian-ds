# Authentication Priority (Jira & Confluence)

## Default Priority

The application tries authentication methods in this order:

```
1. OAuth (if ATLASSIAN_OAUTH_ENABLE=true or ATLASSIAN_OAUTH_CLIENT_ID is set)
2. Personal Access Token (PAT) - Server/Data Center only
3. Basic Auth (JIRA_USERNAME + JIRA_API_TOKEN, etc.)
```

Stop at first successful method - do not fall through.

## Environment Variables by Method

### OAuth
```bash
ATLASSIAN_OAUTH_ENABLE=true
ATLASSIAN_OAUTH_CLIENT_ID=your-client-id
ATLASSIAN_OAUTH_CLIENT_SECRET=your-client-secret
ATLASSIAN_OAUTH_SCOPES=read:jira-work write:jira-work
```

### Personal Access Token (Server/Data Center)
```bash
JIRA_PERSONAL_TOKEN=your-pat-token
CONFLUENCE_PERSONAL_TOKEN=your-pat-token
```

### Basic Auth
```bash
JIRA_USERNAME=your-username
JIRA_API_TOKEN=your-api-token
CONFLUENCE_USERNAME=your-username
CONFLUENCE_API_TOKEN=your-api-token
```

## Key Changes from Upstream

- ❌ **Removed**: Client certificates (`CLIENT_CERT`, `CLIENT_KEY`, `CLIENT_KEY_PASSWORD`)
- ✅ **Added**: OAuth takes global priority (consistent across Cloud/Server/DC)
- ✅ **Simplified**: Single clear priority path (no conflict resolution)

See `PROXY_AND_AUTHENTICATION.md` for proxy setup.

## Troubleshooting

**Q: "Authentication failed" but env vars are set?**
- A: Check priority - higher methods override lower ones. Remove higher-priority methods if not needed.

**Q: OAuth not working?**
- A: Verify `ATLASSIAN_OAUTH_ENABLE=true` AND client ID/secret are set.

**Q: Server/DC needs both PAT and Basic Auth?**
- A: Use PAT (higher priority). Basic auth is fallback only.
