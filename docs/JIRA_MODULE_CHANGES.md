# Jira Module Changes & API Compatibility

## What Changed

### 1. Comment Visibility Removed ❌
**Affected Methods:**
- `add_comment()` - no longer accepts `visibility` parameter
- `edit_comment()` - method completely removed

**Before:**
```python
# Restrict comment to specific group
confluence.add_comment(
    issue_key="PROJ-123",
    comment="Internal note",
    visibility={"type": "group", "value": "jira-users"}
)
```

**After:**
```python
# Comments are now public (no visibility control)
confluence.add_comment(
    issue_key="PROJ-123",
    comment="Internal note"
)
```

**Impact:** Comments cannot be restricted by user group or role. All comments added through this client are visible to all issue watchers.

### 2. Comment Editing Removed ❌
**Affected Method:**
- `edit_comment()` - entire method deleted

**Before:**
```python
confluence.edit_comment(
    issue_key="PROJ-123",
    comment_id="12345",
    comment="Updated note",
    visibility={"type": "group", "value": "jira-users"}
)
```

**After:**
```python
# Comment editing not available through client
# Use Jira UI or direct REST API if needed
```

**Impact:** Comments cannot be edited after creation. Users must use Jira UI or direct HTTP calls to edit comments.

### 3. Client Certificate Authentication Removed ❌
**Affected Class:** `JiraClient`
- `client_cert` parameter removed from initialization
- `client_key` parameter removed
- `client_key_password` parameter removed

**Before:**
```python
config = JiraConfig(
    url="https://jira.company.net",
    client_cert="/path/to/cert.pem",
    client_key="/path/to/key.pem",
    client_key_password="secret"
)
```

**After:**
```python
config = JiraConfig(
    url="https://jira.company.net",
    https_proxy="http://proxy.company.net:8080"
)
# TLS/mTLS handled by proxy layer
```

**Impact:** Certificates must be configured at proxy level (JFrog Artifactory), not in application code. See `PROXY_AND_AUTHENTICATION.md`.

## Migration Guide

| Feature | Workaround |
|---------|-----------|
| Need restricted comments? | Use Jira UI to set visibility manually, or direct REST API call |
| Need to edit comments? | Use Jira UI or `curl` to direct REST API |
| Need client certificates? | Configure at proxy level (JFrog), not in app |

## Why These Changes?

1. **Comment Visibility/Editing**: Advanced permission features, rare use case in typical workflows
2. **Client Certificates**: Security best practice - centralize certificate management at proxy layer
3. **Code Quality**: Reduced complexity, clearer API surface

---

See `FEATURE_SCOPE.md` for full list of supported vs. removed features.
