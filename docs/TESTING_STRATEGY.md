# Testing Strategy: MVP Focus

## Core Operations Only

Integration tests cover **core operations only**:
- ✅ Create, read, update, delete (CRUD)
- ✅ Search and filtering
- ✅ Issue transitions
- ✅ Comment viewing and addition
- ✅ Confluence page operations

## Not Tested

Advanced features removed from MVP:
- ❌ Comment editing (`edit_comment`)
- ❌ Advanced field manipulation
- ❌ SLA/metrics tracking
- ❌ Analytics operations

## For Advanced Features

If you need functionality beyond core operations:

1. **Check REST API directly**
   ```bash
   # Example: Get issue transitions (non-core)
   curl -H "Authorization: Bearer $TOKEN" \
     "https://jira.samsungds.net/rest/api/3/issue/PROJ-123/transitions"
   ```

2. **Extend MCP tools** (if justified)
   - Add to relevant module (`jira/`, `confluence/`)
   - Include integration test
   - Document in `FEATURE_SCOPE.md`

3. **Open issue** with specific use case

## Test Execution

```bash
# Run all tests
pytest tests/

# Run integration tests only (requires real API credentials)
pytest tests/integration/

# Run specific test
pytest tests/integration/test_real_api.py::TestRealJiraAPI::test_get_issue
```

## Environment for Real API Tests

```bash
# In .env:
CONFLUENCE_URL=https://your-company.atlassian.net/wiki
JIRA_URL=https://your-company.atlassian.net
ATLASSIAN_OAUTH_CLIENT_ID=...
ATLASSIAN_OAUTH_CLIENT_SECRET=...
# or use API tokens
```

---

See `FEATURE_SCOPE.md` for what's supported.
