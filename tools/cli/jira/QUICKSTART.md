# 🚀 DS JIRA CLI - Quick Start Guide

**Created**: 2026-02-25
**Status**: ✅ Ready for Development & Testing
**Purpose**: Internal JIRA testing + Claude collaboration

---

## 📁 Directory Structure

```
tools/cli/
├── __init__.py                      # Package init
├── main.py                          # CLI entry point (Click app)
├── README.md                        # Full documentation
├── QUICKSTART.md                    # This file
├── commands/
│   ├── __init__.py                  # Command group setup
│   └── jira.py                      # JIRA commands (3 main + 1 bonus)
└── utils/
    ├── __init__.py
    ├── config.py                    # JIRA config from env vars
    └── formatter.py                 # Output formatters (json, yaml, table)
```

---

## 🎯 3 Main CLI Commands

### 1️⃣ `create` - Create a New Issue

```bash
# Syntax
jira-cli create --project KEY --type TYPE --summary "Summary text"

# Examples
jira-cli create --project PROJ --type Task --summary "Fix API endpoint"
jira-cli create --project ABC --type Bug --summary "Login fails" --format table
jira-cli create --project PROJ --type Story --summary "New feature" \
  --description "Add this feature" --assignee john.doe
```

**Options:**
- `--project KEY` (required): Project key (e.g., PROJ, ABC)
- `--type TYPE` (required): Issue type (e.g., Task, Bug, Story)
- `--summary TEXT` (required): Issue title
- `--description TEXT` (optional): Issue description
- `--assignee USERNAME` (optional): Assignee username
- `--format json|yaml|table` (optional): Output format

---

### 2️⃣ `read` - Read Issue Details

```bash
# Syntax
jira-cli read ISSUE_KEY

# Examples
jira-cli read PROJ-123
jira-cli read PROJ-123 --format table
jira-cli read PROJ-123 --fields summary,status,assignee
jira-cli read ABC-456 --format yaml
```

**Options:**
- `ISSUE_KEY` (required): Issue key (e.g., PROJ-123)
- `--fields FIELDS` (optional): Comma-separated field names
- `--format json|yaml|table` (optional): Output format
- `--verbose` (optional): Enable debug logging

---

### 3️⃣ `custom_field get` - Get Custom Field Info

Query JIRA API (`GET /rest/api/2/field`) to get field details:

```bash
# Syntax
jira-cli custom_field get FIELD_ID

# Examples
jira-cli custom_field get customfield_10201
jira-cli custom_field get customfield_10201 --format table
jira-cli custom_field get customfield_10203 --verbose
```

**Options:**
- `FIELD_ID` (required): Custom field ID (e.g., customfield_10201)
- `--format json|yaml|table` (optional): Output format
- `--verbose` (optional): Enable debug logging

**Response Example:**
```json
{
  "id": "customfield_10201",
  "name": "Epic Link",
  "schema": {
    "type": "issue",
    "custom": "com.pyxis.greenhopper.jira:gh-epic-link"
  },
  "searchable": true,
  "editable": true
}
```

---

## 🎁 Bonus: Additional Commands (Already Included!)

### List All Custom Fields

```bash
# List first 20 fields
jira-cli custom_field list

# List more
jira-cli custom_field list --limit 50

# Search for "epic"
jira-cli custom_field list --search epic --format table

# Combine
jira-cli custom_field list --search epic --limit 10 --format table
```

---

## 🔐 Setup (First Time)

### 1. Set Environment Variables

```bash
export JIRA_URL="https://jira.samsungds.net"
export JIRA_PERSONAL_TOKEN="your_personal_access_token"
```

**Important**: Variable names are synchronized with `.env.example` (SSOT)

### 2. Run CLI

#### 🏢 **Internal (사내):**
```bash
# Via uv (from project root)
cd /home/bwyoon/para/project/jira-mcp/mcp-atlassian-ds
uv run python -m tools.cli.jira --help

# After installation
jira-cli --help
jira-cli create --help
jira-cli read --help
```

#### 🌍 **External (외부) - WITH SSL FIX:**
```bash
# Use --native-tls flag to bypass SSL certificate issues
uv run --native-tls --project pyproject.external.toml python -m tools.cli.jira --help

# This solves: "invalid peer certificate: UnknownIssuer"
```

---

## 📊 Output Formats

### JSON (Default)
```bash
jira read PROJ-123
# Output: Pretty-printed JSON (2-space indent)
```

### Table
```bash
jira read PROJ-123 --format table
jira custom_field list --format table
# Output: ASCII table (best for terminal)
```

### YAML
```bash
jira read PROJ-123 --format yaml
# Output: YAML format (if PyYAML installed)
```

---

## 🧪 Development & Testing Workflow

### 1. Run Command
```bash
jira custom_field get customfield_10201
```

### 2. Share Result with Claude
Copy-paste the JSON output to Claude for analysis/discussion.

### 3. Iterate Together
- Discuss results
- Modify command options
- Test different field IDs
- Debug issues together

---

## 💡 Tips for Developers

### Use Verbose Mode for Debugging
```bash
jira custom_field get customfield_10201 --verbose
# Shows detailed logs and configuration
```

### Pipe to jq for JSON Processing
```bash
# Extract just the field name
jira custom_field get customfield_10201 | jq '.name'
# Output: "Epic Link"

# List and filter fields
jira custom_field list | jq '.fields[] | select(.name | contains("Epic"))'
```

### Create Aliases for Shortcuts
```bash
# Add to ~/.bashrc or ~/.zshrc
alias jira-epic='jira custom_field get customfield_10201'
alias jira-fields='jira custom_field list --format table'
```

### Test with Different Formats
```bash
# Always test with different formats to understand data
jira custom_field get customfield_10201 --format json
jira custom_field get customfield_10201 --format table
jira custom_field get customfield_10201 --format yaml
```

---

## 🆘 Troubleshooting

### Issue: "Invalid JIRA configuration"
**Solution**: Check environment variables
```bash
echo $JIRA_URL
echo $JIRA_PAT
# Set if missing
export JIRA_URL="https://jira.example.com"
export JIRA_PAT="your_token"
```

### Issue: "Field not found"
**Solution**: List available fields
```bash
jira custom_field list --format table
jira custom_field list --search epic
```

### Issue: "JiraClient import failed"
**Solution**: Ensure package is installed
```bash
cd /home/bwyoon/para/project/diff-mcp/mcp-atlassian-ds
uv pip install -e .
# Then try again
uv run python -m tools.cli jira --help
```

---

## 📝 Common Field IDs Reference

| Field ID | Name | Use Case |
|----------|------|----------|
| `customfield_10201` | Epic Link | Link issues to epics |
| `customfield_10203` | Epic Name | Epic name/label |
| `customfield_11106` | Start date (WBSGantt) | Project start |
| `customfield_11107` | Finish date (WBSGantt) | Project end |
| `customfield_15500` | 팀명 | Team name |

---

## 🚀 Next Steps

1. ✅ Set up environment variables
2. ✅ Run `jira --help` to verify installation
3. ✅ Try: `jira custom_field get customfield_10201`
4. ✅ Share result with Claude
5. ✅ Test other commands and formats

---

## 📚 Full Documentation

See `README.md` for:
- Complete command reference
- All options and examples
- Output format details
- Development guidelines
- Planned future commands

---

## ❓ Questions?

- Run `jira --help` for overview
- Run `jira jira --help` for JIRA commands
- Run `jira jira create --help` for specific command help
- See `README.md` for detailed documentation
