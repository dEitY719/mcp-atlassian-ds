# Confluence Module Changes & API Compatibility

## What Changed

### 1. Page Emoji Removed ❌
**Affected Methods:**
- `create_page()` - no longer accepts `emoji` parameter
- `update_page()` - no longer accepts `emoji` parameter
- `get_page_content()` - no longer returns `emoji` field
- `get_page_by_title()` - no longer returns `emoji` field

**Before:**
```python
page = confluence.create_page(space_key="PROJ", title="Page", body="...", emoji="📝")
```

**After:**
```python
page = confluence.create_page(space_key="PROJ", title="Page", body="...")
# emoji parameter is removed - page will use Confluence default
```

### 2. Child Pages Only (No Folders) ❌
**Affected Method:**
- `get_child_pages()` - no longer accepts `include_folders` parameter
- Returns only child pages, not folders

**Before:**
```python
children = confluence.get_child_pages(page_id, include_folders=True)
# Returns both child pages and folders
```

**After:**
```python
children = confluence.get_child_pages(page_id)
# Returns only child pages
```

### 3. Removed Utility Functions ❌
Dead code removal in `confluence/utils.py`:
- `extract_emoji_from_property()` - emoji parsing
- `emoji_to_hex_id()` - emoji to hex conversion

**Impact:** If you were using these directly, they no longer exist.

### 4. Removed V2 API Methods (OAuth) ❌
**Affected Class:** `ConfluenceV2Adapter`
- `get_page_emoji()` - retrieve emoji from content properties
- `set_page_emoji()` - set/remove page emoji
- `_set_page_property()` - helper for setting properties
- `_get_property()` - helper for retrieving properties
- `get_page_views()` - get page view statistics

**Impact:** OAuth users (Cloud Confluence) no longer have emoji or analytics support.

### 5. Analytics Mixin Removed ❌
**Affected Class:** `ConfluenceFetcher`
- `AnalyticsMixin` - no longer available in main ConfluenceFetcher
- Page view analytics, metrics, engagement tracking removed

**Before:**
```python
from mcp_atlassian.confluence import ConfluenceFetcher
fetcher = ConfluenceFetcher(...)  # Had AnalyticsMixin
```

**After:**
```python
from mcp_atlassian.confluence import ConfluenceFetcher
fetcher = ConfluenceFetcher(...)  # No analytics support
```

**Impact:** Cloud Confluence users cannot track page views, engagement metrics, or performance analytics through this client.

## Migration Guide

| Feature | Workaround |
|---------|-----------|
| Need emoji on pages? | Use Confluence UI to set manually, or update API call directly |
| Need folder support? | Use Confluence spaces instead of nested folders |
| Need page properties? | Direct HTTP call to Confluence REST API |

## Code Removals Summary

```
confluence/pages.py:     -214 lines (emoji + folder logic)
confluence/utils.py:     -56 lines (emoji utility functions)
confluence/v2_adapter.py: -206 lines (emoji + analytics for OAuth)
Total:                   -476 lines
```

## Why These Changes?

1. **Emoji**: Decorative feature, not functional
2. **Folders**: Confluence spaces provide organization
3. **Code Quality**: Removed dead code, reduced complexity

---

See `FEATURE_SCOPE.md` for full list of supported vs. removed features.
