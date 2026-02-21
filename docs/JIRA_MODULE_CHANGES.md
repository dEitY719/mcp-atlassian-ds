# Jira Module Changes & API Compatibility

## What Changed

### 1. Comment Visibility Removed ❌
**Affected Methods:**
- `add_comment()` - no longer accepts `visibility` parameter
- `edit_comment()` - method completely removed

**Supported Operations:**
- ✅ `get_issue_comments()` - retrieve all comments (public only)
- ✅ `add_comment()` - add new comment (public only)
- ❌ Restrict comment visibility (removed)
- ❌ Edit comments (removed)

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

**Note:** Comment field is automatically included in issue details. When you fetch an issue, comments are included by default (no separate call needed).

**Impact:**
- Comments cannot be restricted by user group or role
- All comments added through this client are visible to all issue watchers
- All comments are public/unrestricted

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
**Affected Class:** `JiraClient` & `JiraConfig`
- `client_cert` parameter removed from config
- `client_key` parameter removed
- `client_key_password` parameter removed
- Environment variables no longer read: `JIRA_CLIENT_CERT`, `JIRA_CLIENT_KEY`, `JIRA_CLIENT_KEY_PASSWORD`

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

### 4. SLA Configuration Removed ❌
**Affected Classes:** `SLAConfig` (entire class deleted), `JiraConfig.sla_config` field

**Before:**
```python
config = JiraConfig(
    url="https://jira.company.net",
    sla_config=SLAConfig(
        default_metrics=["cycle_time", "time_in_status"],
        working_hours_only=True,
        working_hours_start="09:00",
        working_hours_end="17:00",
        working_days=[1,2,3,4,5],
        timezone="Asia/Seoul"
    )
)
```

**After:**
```python
config = JiraConfig(
    url="https://jira.company.net"
)
# SLA features not available
```

**Impact:** SLA metrics, working hours, and advanced time calculations are no longer supported through this client. Use direct Jira REST API or Insight Cloud if needed.

### 5. Markup Translation Config Removed ❌
**Affected Field:** `JiraConfig.disable_jira_markup_translation`
- Environment variable `DISABLE_JIRA_MARKUP_TRANSLATION` no longer read

**Impact:** Text preprocessing now always converts Markdown → Jira markup. Cannot disable this behavior.

## Migration Guide

| Feature | Workaround |
|---------|-----------|
| Need restricted comments? | Use Jira UI to set visibility manually, or direct REST API call |
| Need to edit comments? | Use Jira UI or `curl` to direct REST API |
| Need client certificates? | Configure at proxy level (JFrog), not in app |

## Implementation Notes

### Epic Field Detection (Important for Troubleshooting)
Epic fields vary significantly across Jira instances:
- **Samsung DS Jira**: customfield_10203 (Epic Name), customfield_10201 (Epic Link)
- **Jira Cloud**: customfield_10014, customfield_10008
- **Jira Server**: customfield_10011, customfield_10005

The client attempts multiple strategies:
1. Dynamic discovery from existing epics (most reliable)
2. Standard field names (epic_link, Epic Link, etc.)
3. Common custom field IDs (by frequency)

**If epic linking fails:**
- The error message will show which fields were tried
- Check your Jira instance's custom field configuration
- Contact your Jira admin to map epic fields correctly

## Why These Changes?

1. **Comment Visibility/Editing**: Advanced permission features, rare use case in typical workflows
2. **Client Certificates**: Security best practice - centralize certificate management at proxy layer
3. **Code Quality**: Reduced complexity, clearer API surface

---

See `FEATURE_SCOPE.md` for full list of supported vs. removed features.
