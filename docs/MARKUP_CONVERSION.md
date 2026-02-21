# Markup Conversion: Markdown ↔ Jira/Confluence

## Text Preprocessing

### Jira Markup (Markdown → Jira Syntax)

**Always enabled.** Cannot be disabled.

```python
from mcp_atlassian.preprocessing import JiraPreprocessor

preprocessor = JiraPreprocessor(base_url="https://jira.samsungds.net")

# Markdown → Jira Markup
markdown = "# Heading\n\n**bold** text *italic*"
jira = preprocessor.markdown_to_jira(markdown)
# Result: "h1. Heading\n\n*bold* text _italic_"
```

### Confluence Storage Format (Markdown → HTML)

**Always enabled.** Cannot be disabled.

```python
from mcp_atlassian.preprocessing import ConfluencePreprocessor

preprocessor = ConfluencePreprocessor(base_url="https://confluence.samsungds.net")

# Markdown → Confluence Storage Format (HTML)
markdown = "# Heading\n\n**bold** text"
storage = preprocessor.markdown_to_confluence_storage(markdown)
# Result: "<h1>Heading</h1><p><strong>bold</strong> text</p>"
```

## What Changed

### `disable_translation` Removed ❌

**Before:**
```python
# Could disable markup translation
preprocessor = JiraPreprocessor(
    base_url="...",
    disable_translation=True  # Pass through without conversion
)
```

**After:**
```python
# Markup translation always happens
preprocessor = JiraPreprocessor(base_url="...")
# No option to disable - pass through without conversion not supported
```

**Impact:** All Markdown is converted to Jira/Confluence markup. No passthrough mode.

### Edge Case Handling Removed ❌

Issue #786 regression tests removed:
- Header syntax validation (# requires space)
- Special handling for Jira list syntax preservation
- md2conf API fallback for compatibility

**Impact:**
- Standard Markdown rules apply (not forgiving)
- `# text` (no space) = invalid Markdown, not converted
- Jira lists in source must be valid

### Standard Library Only

**Before:**
```python
# md2conf fallback if primary API failed
from mcp_atlassian.preprocessing.confluence import elements_from_string
```

**After:**
```python
# Standard md2conf library only (no fallback)
# Elements parsing is md2conf responsibility
```

**Impact:** Relies on md2conf library's default behavior, no custom fallbacks.

## Supported Conversions

### Jira Markup Support

| Markdown | Jira Output |
|----------|-------------|
| `# Heading` | `h1. Heading` |
| `## Subheading` | `h2. Subheading` |
| `**bold**` | `*bold*` |
| `*italic*` | `_italic_` |
| `[link](url)` | `[link\|url]` |
| `- List item` | `* List item` |

### Confluence Storage Support

| Markdown | HTML Output |
|----------|-------------|
| `# Heading` | `<h1>Heading</h1>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `[link](url)` | `<a href="url">link</a>` |

## Common Issues

**Q: My Markdown doesn't convert correctly?**
- A: Check for valid Markdown syntax (e.g., `# ` with space for headers)
- Invalid syntax is silently ignored

**Q: Can I disable markup conversion?**
- A: No. Conversion is always active. Use preprocessor methods to bypass if needed.

**Q: How do I add custom markup rules?**
- A: Extend `JiraPreprocessor` or `ConfluencePreprocessor` class

---

See `JIRA_MODULE_CHANGES.md` section "Markup Translation Config Removed" for details.
