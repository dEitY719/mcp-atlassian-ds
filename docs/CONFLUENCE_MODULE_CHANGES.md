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

## Migration Guide

| Feature | Workaround |
|---------|-----------|
| Need emoji on pages? | Use Confluence UI to set manually, or update API call directly |
| Need folder support? | Use Confluence spaces instead of nested folders |
| Need page properties? | Direct HTTP call to Confluence REST API |

## Code Removals Summary

```
confluence/pages.py:  -214 lines (emoji + folder logic)
confluence/utils.py:  -56 lines (emoji utility functions)
Total:               -270 lines
```

## Why These Changes?

1. **Emoji**: Decorative feature, not functional
2. **Folders**: Confluence spaces provide organization
3. **Code Quality**: Removed dead code, reduced complexity

---

See `FEATURE_SCOPE.md` for full list of supported vs. removed features.
