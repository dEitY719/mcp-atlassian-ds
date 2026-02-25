# 🔧 DS JIRA CLI - Setup & Usage Guide

**Created**: 2026-02-25
**Location**: `/home/bwyoon/para/project/diff-mcp/mcp-atlassian-ds/tools/cli/`
**Status**: ✅ Development Ready

---

## 📋 Overview

A **developer-friendly CLI** for testing JIRA operations and collaborating with Claude on results.

```
┌─────────────────────────────────────┐
│  You (samsungds internal network)    │
│  Run: jira custom_field get ...      │
└────────────────┬────────────────────┘
                 │
                 ├─→ Copy JSON output
                 │
┌────────────────▼────────────────────┐
│  Claude (external PC via web)       │
│  Analyze results & discuss          │
│  Plan next commands together        │
└─────────────────────────────────────┘
```

---

## 🎯 What You Get

### 3 Main Commands

| Command | Purpose | Example |
|---------|---------|---------|
| **`jira create`** | Create JIRA issue | `jira create --project PROJ --type Task --summary "..."` |
| **`jira read`** | Get issue details | `jira read PROJ-123` |
| **`jira custom_field get`** | Query JIRA REST API (`/rest/api/2/field`) | `jira custom_field get customfield_10201` |

### Bonus Features

- ✅ Multiple output formats: **JSON** (default), **YAML**, **Table**
- ✅ Custom field search and listing
- ✅ Verbose mode for debugging
- ✅ Clear help text and error messages
- ✅ Environment variable configuration

---

## 📁 Directory Structure

```
mcp-atlassian-ds/
├── src/mcp_atlassian/              ← Original library (unchanged)
│   ├── jira/
│   ├── confluence/
│   └── ...
├── tools/cli/                       ← NEW: Development CLI
│   ├── __init__.py
│   ├── main.py                      # Entry point
│   ├── README.md                    # Full documentation
│   ├── QUICKSTART.md                # Quick reference
│   ├── commands/
│   │   ├── __init__.py
│   │   └── jira.py                  # 3 commands implemented
│   └── utils/
│       ├── config.py                # Config management
│       └── formatter.py             # Output formatters
└── JIRA_CLI_SETUP.md                ← This file
```

### Why `tools/cli/`?

✅ **Separated from core library** - original `src/mcp_atlassian/` stays clean
✅ **Independent development** - no conflicts with `mcp-atlassian` upstream
✅ **Easy migration later** - can move to `jiravis/backend/cli/` when ready
✅ **Clear responsibility** - Library vs. Tool distinction

---

## 🚀 Getting Started

### Step 1: Set Environment Variables

```bash
# Option A: Personal Access Token (Recommended)
export JIRA_URL="https://jira.example.com"
export JIRA_PAT="your_personal_access_token"

# Option B: Basic Auth
export JIRA_URL="https://jira.example.com"
export JIRA_USERNAME="username"
export JIRA_PASSWORD="password"
```

### Step 2: Run a Command

```bash
cd /home/bwyoon/para/project/diff-mcp/mcp-atlassian-ds

# Via uv (recommended for development)
uv run python -m tools.cli jira custom_field get customfield_10201

# After installation
jira custom_field get customfield_10201
```

### Step 3: Share Result with Claude

```bash
# Copy the JSON output
jira custom_field get customfield_10201

# Paste to Claude:
# "Hey Claude, I got this result:
#  [paste JSON here]
#  Is this what we expected?"
```

---

## 📖 Examples

### Get Custom Field Information

```bash
# Query JIRA REST API GET /rest/api/2/field
jira custom_field get customfield_10201

# Response:
# {
#   "id": "customfield_10201",
#   "name": "Epic Link",
#   "schema": {
#     "type": "issue",
#     "custom": "com.pyxis.greenhopper.jira:gh-epic-link"
#   },
#   "searchable": true,
#   "editable": true
# }
```

### Create an Issue

```bash
# Simple
jira create --project PROJ --type Task --summary "Fix API"

# With description
jira create \
  --project PROJ \
  --type Bug \
  --summary "Login fails on mobile" \
  --description "Users cannot login from mobile" \
  --assignee john.doe
```

### Read Issue Details

```bash
# All fields
jira read PROJ-123

# Specific fields as table
jira read PROJ-123 --fields summary,status,assignee --format table

# As YAML
jira read PROJ-123 --format yaml
```

---

## 🎨 Output Formats

### JSON (Default - Best for Sharing)

```bash
jira custom_field get customfield_10201
```

**Use when:**
- Sharing with Claude
- Processing with `jq`
- Storing results
- Programmatic use

### Table (Best for Terminal)

```bash
jira custom_field get customfield_10201 --format table
jira custom_field list --format table
```

**Use when:**
- Quick visual inspection
- Reading in terminal
- Comparing multiple items

### YAML (Best for Readability)

```bash
jira custom_field get customfield_10201 --format yaml
```

**Use when:**
- Human-readable output
- Configuration files
- Documentation

---

## 🔧 Architecture Overview

```python
# tools/cli/commands/jira.py defines:

@jira_group.command(name="create")
def create_issue(...): ...              # 1️⃣ Create JIRA issue

@jira_group.command(name="read")
def read_issue(...): ...                # 2️⃣ Read issue details

@custom_field_group.command(name="get")
def get_custom_field(...): ...          # 3️⃣ Get custom field

@custom_field_group.command(name="list")
def list_custom_fields(...): ...        # 🎁 Bonus: List fields
```

### Design Principles

✅ **Click Framework**: Standard Python CLI framework
✅ **Context Management**: Shared configuration across commands
✅ **Error Handling**: Clear error messages with suggestions
✅ **Extensible**: Easy to add new commands
✅ **Developer-Friendly**: Help text with examples

---

## 💾 Key Files

### Entry Points

| File | Purpose | Run With |
|------|---------|----------|
| `tools/cli/main.py` | Main CLI app | `python -m tools.cli` |
| `tools/cli/commands/jira.py` | JIRA commands | (imported by main) |

### Configuration

| File | Purpose |
|------|---------|
| `tools/cli/utils/config.py` | Read env vars → JIRA config |
| `tools/cli/utils/formatter.py` | Format output (JSON/YAML/Table) |

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Full documentation + reference |
| `QUICKSTART.md` | Quick reference (5 min read) |
| `JIRA_CLI_SETUP.md` | This file - overview + setup |

---

## 🚀 Typical Development Workflow

```
1. Design command with Claude
   "How should 'jira create' work?"

2. Set up environment
   export JIRA_URL=...
   export JIRA_PAT=...

3. Run CLI command
   jira custom_field get customfield_10201

4. Get JSON output
   {
     "id": "customfield_10201",
     "name": "Epic Link",
     ...
   }

5. Share with Claude
   [Paste JSON + ask for feedback]

6. Claude helps debug
   "The 'schema' field is missing. Let's check if..."

7. Iterate together
   Test other commands, formats, field IDs
```

---

## ⚙️ Technical Details

### Technologies Used

- **Click**: CLI framework (already in pyproject.toml)
- **Python 3.10+**: Type hints, modern Python
- **PyYAML**: Optional (for YAML output)

### Type Safety

- ✅ Full type hints
- ✅ MyPy compatible
- ✅ Pydantic for data validation (config.py)

### Error Handling

- ✅ Clear error messages
- ✅ Suggestions for common issues
- ✅ Verbose mode for debugging
- ✅ Graceful fallbacks (e.g., YAML → JSON)

---

## 🎁 Why This Structure?

### Original Concern
> "If I add CLI to mcp-atlassian-ds, it will diff from original mcp-atlassian"

### Our Solution
```
tools/                  ← Completely separate from src/
├── cli/                ← Only company's CLI tools
└── (future)            ← Other tools here

src/mcp_atlassian/      ← Original library (unchanged)
```

**Benefits:**
1. ✅ Original `src/` stays clean
2. ✅ No conflicts when syncing from upstream
3. ✅ Easy to migrate CLI to jiravis/backend later
4. ✅ Clear separation of concerns

---

## 📚 Documentation Files

### Quick Reference
- **`tools/cli/QUICKSTART.md`** - 5-minute quick start

### Full Reference
- **`tools/cli/README.md`** - Complete documentation with all examples

### Setup Guide
- **This file (`JIRA_CLI_SETUP.md`)** - Overview and rationale

---

## 🎯 Future Enhancements (Planned)

### Phase 2: More Commands
```bash
jira update PROJ-123 --status "In Progress"
jira search "assignee = currentUser()"
jira transition PROJ-123 --to Done
```

### Phase 3: Confluence Commands
```bash
confluence create --space SPACE --title "Page"
confluence read PAGE_ID
confluence search --keyword "team"
```

### Phase 4: Integration
```bash
# Eventually: auto-integration with jiravis/backend
jira agent --prompt "Show me all open issues"
```

---

## ✅ Checklist

- [x] Created `/tools/cli/` directory structure
- [x] Implemented 3 main commands + 1 bonus
- [x] Added multi-format output (JSON/YAML/Table)
- [x] Created comprehensive documentation
- [x] Added to `pyproject.toml` entry points
- [x] Verified Python syntax
- [ ] Test with actual JIRA instance (next step!)
- [ ] Get feedback from teammates
- [ ] Add unit tests
- [ ] Publish to internal wiki/docs

---

## 📞 Next Steps

### 1. Test in Your Environment

```bash
cd /home/bwyoon/para/project/diff-mcp/mcp-atlassian-ds
export JIRA_URL="https://your-jira.com"
export JIRA_PAT="your-token"

# Test the command
jira custom_field get customfield_10201
```

### 2. Share Results with Claude

Copy the JSON output and share with Claude.

### 3. Iterate Together

- Discuss results
- Modify commands
- Add new features
- Fix issues

### 4. Document and Share

Add findings to team documentation.

---

## 🔗 Related Files

- **Original Project**: `README.md` (parent directory)
- **Architecture**: `docs/PROJECT-WORK-FLOW.md` (jiravis)
- **Authentication**: `docs/PROXY_AND_AUTHENTICATION.md`
- **Custom Fields**: `README.md` (lines 138-161)

---

## 💡 Pro Tips

### 1. Use Aliases for Common Tasks
```bash
# Add to ~/.bashrc
alias jira-epic='jira custom_field get customfield_10201'
alias jira-fields='jira custom_field list --format table'
```

### 2. Pipe to jq for JSON Processing
```bash
jira custom_field get customfield_10201 | jq '.name'
# Output: "Epic Link"
```

### 3. Always Test New Fields
```bash
# First: JSON to see raw data
jira custom_field get FIELD_ID

# Then: Table to see formatted output
jira custom_field get FIELD_ID --format table

# Then: Discuss with Claude
# "Is this the right field?"
```

---

**Status**: ✅ Ready to use!
**Contact**: For questions, share with Claude
**Last Updated**: 2026-02-25
