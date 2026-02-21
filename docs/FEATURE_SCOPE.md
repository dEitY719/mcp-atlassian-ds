# Feature Scope: What's Included & What's Not

## Confluence Page Management

### ✅ Supported Operations

**Core Page Operations:**
- Get page content (`get_page_content()`)
- Get page by title (`get_page_by_title()`)
- Create pages (`create_page()`)
- Update pages (`update_page()`)
- Get child pages (`get_child_pages()`)
- Search pages

**Content Formats:**
- HTML storage format (native)
- Markdown (auto-converted)
- Support for expand parameters (version, space, children)

### ❌ Removed Features

**Why removed:**
These are "nice-to-have" features, not core operations. Removing them reduces:
- Code complexity (90+ lines removed)
- Maintenance burden
- External dependencies
- Learning curve for new developers

**Removed:**
| Feature | Why Removed |
|---------|------------|
| Page emoji icons | Decorative, not functional |
| Folder hierarchies | Namespace/organization (use spaces instead) |
| Content properties | Advanced use case |
| Property value setting | Edge case handling |
| Page view analytics | Cloud-only feature, not required for core operations |

## Jira Issue Management

### ✅ Supported Operations
- Create issues
- Search/filter issues
- Get issue details
- Update issues
- Transition issues
- Add comments
- Get comments
- Get transitions

### ❌ Not Included
- Sprints / Agile boards
- Metrics / Velocity tracking
- SLA monitoring
- Advanced Automation rules
- Comment visibility restrictions
- Comment editing
- Worklog time tracking
- Client certificate authentication (use proxy instead)

## General Philosophy

**Samsung DS mcp-atlassian focuses on:**
```
Core Operations > Advanced Features
Maintainability > Feature Completeness
Developer Experience > Flexibility
```

**When You Need Advanced Features:**
1. Check if there's a REST API endpoint
2. Use direct HTTP calls to Jira/Confluence API
3. Open an issue with specific use case

---

See docs/ for setup, authentication, and troubleshooting guides.
