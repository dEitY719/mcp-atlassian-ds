# 🔧 DS JIRA CLI - Developer-Friendly Command-Line Interface

A modern, developer-friendly CLI for interacting with JIRA instances. Test JIRA operations quickly and share results with teammates.

## ✨ Features

- **📝 Create Issues**: Quickly create JIRA issues from the command line
- **📖 Read Issues**: Fetch issue details with flexible field selection
- **🔧 Manage Custom Fields**: Query JIRA's REST API to discover and manage custom fields
- **🎨 Multiple Output Formats**: JSON (default), YAML, and Table formats
- **🔐 Secure Authentication**: Supports PAT (Personal Access Token) and basic auth
- **🚀 Developer-Friendly**: Clear error messages, helpful `--help` text, verbose mode

## 📋 Prerequisites

- Python 3.10+
- mcp-atlassian-ds installed and configured
- Environment variables set for JIRA authentication

## 🔐 Setup Authentication

Choose one authentication method:

### Personal Access Token Authentication

```bash
export JIRA_URL="https://jira.samsungds.net"
export JIRA_PERSONAL_TOKEN="your_personal_access_token"
```

**Get your PAT from JIRA:**
1. Click your profile icon (top right)
2. Go to **Profile** → **Personal Access Tokens**
3. Click **Create Token** → **Confirm**
4. Copy the generated token

### Optional: API Version

```bash
export JIRA_API_VERSION="2"  # Default: 2 (Jira Server/DC)
# Use "3" for Jira Cloud v2 API
```

## 🚀 Quick Start

### Install CLI

```bash
cd /path/to/mcp-atlassian-ds

# Run via uv
uv run python -m tools.cli --help

# Or install and run directly
uv pip install -e .
jira --help
```

### Basic Commands

#### 1️⃣ Create an Issue

```bash
# Simple creation
jira create --project PROJ --type Task --summary "Fix API endpoint"

# With description and assignee
jira create \
  --project PROJ \
  --type Bug \
  --summary "Login fails on mobile" \
  --description "Users cannot login from mobile devices" \
  --assignee john.doe

# Output as table
jira create --project PROJ --type Task --summary "Task" --format table
```

#### 2️⃣ Read Issue Details

```bash
# Basic read
jira read PROJ-123

# With specific fields
jira read PROJ-123 --fields summary,status,assignee,created

# As table format
jira read PROJ-123 --format table

# As YAML
jira read PROJ-123 --format yaml

# Verbose mode for debugging
jira read PROJ-123 --verbose
```

#### 3️⃣ Get Custom Field Information

Get field details by ID (queries `GET /rest/api/2/field`):

```bash
# Get field info
jira custom_field get customfield_10201

# As table
jira custom_field get customfield_10201 --format table

# Verbose output
jira custom_field get customfield_10201 --verbose
```

Example response:
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

#### 4️⃣ List Custom Fields

List and search all custom fields:

```bash
# List first 20 custom fields
jira custom_field list

# List more fields
jira custom_field list --limit 50

# Search for "epic" related fields
jira custom_field list --search epic

# Table format
jira custom_field list --format table

# Combine options
jira custom_field list --search "epic" --format table --limit 10
```

## 📚 Command Reference

### Global Options

```bash
--help              Show help message
--version           Show version
```

### `jira create`

Create a new JIRA issue.

```bash
jira create --project KEY --type TYPE --summary "Summary" [OPTIONS]

Options:
  --project TEXT          Project key (required)
  --type TEXT             Issue type (required) - e.g., Task, Bug, Story
  --summary TEXT          Issue summary (required)
  --description TEXT      Issue description (optional)
  --assignee USERNAME     Assignee username (optional)
  --format CHOICE         Output format: json, yaml, table (default: json)
  --verbose               Enable verbose logging
```

### `jira read`

Read JIRA issue details.

```bash
jira read ISSUE_KEY [OPTIONS]

Options:
  --fields FIELDS         Comma-separated field names to include
  --format CHOICE         Output format: json, yaml, table (default: json)
  --verbose               Enable verbose logging

Example:
  jira read PROJ-123 --fields summary,status,assignee,created
```

### `jira custom_field get`

Get custom field information by ID.

```bash
jira custom_field get FIELD_ID [OPTIONS]

Options:
  --format CHOICE         Output format: json, yaml, table (default: json)
  --verbose               Enable verbose logging

Example:
  jira custom_field get customfield_10201
  jira custom_field get customfield_10203 --format table
```

### `jira custom_field list`

List all custom fields with optional search.

```bash
jira custom_field list [OPTIONS]

Options:
  --limit N               Maximum fields to list (default: 20)
  --search KEYWORD        Search by field name or ID
  --format CHOICE         Output format: json, yaml, table (default: json)
  --verbose               Enable verbose logging

Example:
  jira custom_field list --format table
  jira custom_field list --search "epic" --limit 50
```

## 🎨 Output Formats

### JSON (Default)

Best for:
- Programmatic processing
- Sharing results with teammates
- Piping to other tools

```bash
jira read PROJ-123
# Output: Pretty-printed JSON
```

### Table

Best for:
- Quick visual inspection
- Terminal output
- Readable reports

```bash
jira read PROJ-123 --format table
```

### YAML

Best for:
- Configuration files
- Human-readable structured data

```bash
jira read PROJ-123 --format yaml
```

## 🔍 Tips & Tricks

### 1. Chain Commands with Other Tools

```bash
# Get field info and parse with jq
jira custom_field get customfield_10201 | jq '.name'

# List and filter fields
jira custom_field list --format json | jq '.fields[] | select(.name | contains("Epic"))'
```

### 2. Create Aliases for Common Tasks

```bash
# In ~/.bashrc or ~/.zshrc
alias jira-epic='jira custom_field get customfield_10201'
alias jira-list='jira custom_field list --format table'
```

### 3. Test Before Production

```bash
# Always test with --format table first
jira create --project TEST --type Task --summary "Test" --format table

# Then check JSON output
jira create --project TEST --type Task --summary "Test" --format json
```

### 4. Use Verbose Mode for Debugging

```bash
# Get detailed logs
jira custom_field get customfield_10201 --verbose

# Check your config
jira custom_field list --verbose 2>&1 | grep "JIRA"
```

## 📝 Common Field IDs (DS JIRA)

Reference: See `README.md` in parent directory for complete list.

| Field ID | Name | Purpose |
|----------|------|---------|
| `customfield_10201` | Epic Link | Link issues to epics |
| `customfield_10203` | Epic Name | Epic name/label |
| `customfield_11106` | Start date (WBSGantt) | Project start date |
| `customfield_11107` | Finish date (WBSGantt) | Project end date |
| `customfield_15500` | 팀명 | Team name |

## 🐛 Troubleshooting

### "Invalid JIRA configuration"

```bash
# Check environment variables
echo $JIRA_URL
echo $JIRA_PAT
# or
echo $JIRA_USERNAME

# Set if missing
export JIRA_URL="https://jira.example.com"
export JIRA_PAT="your_token"
```

### "JiraClient import failed"

```bash
# Ensure mcp-atlassian-ds is installed
uv pip install -e /path/to/mcp-atlassian-ds

# Or run via uv
uv run python -m tools.cli jira --help
```

### "Field not found"

```bash
# List available fields
jira custom_field list --format table

# Search for field
jira custom_field list --search "epic"
```

### "Authentication failed"

```bash
# Verify token is valid
# Check PAT hasn't expired
# Ensure JIRA_URL is correct (no trailing slash)

# Debug with verbose mode
jira custom_field list --verbose
```

## 🚀 Development

### Project Structure

```
tools/cli/
├── main.py              # CLI entry point
├── commands/
│   ├── __init__.py      # Command group registration
│   └── jira.py          # JIRA commands
├── utils/
│   ├── config.py        # Configuration management
│   └── formatter.py     # Output formatters
└── README.md            # This file
```

### Adding New Commands

1. Add new function to `commands/jira.py`
2. Decorate with `@jira_group.command()`
3. Add `--help` text with examples
4. Update this README

Example:

```python
@jira_group.command(name="new-command")
@click.argument("argument", metavar="ARG")
@click.option("--option", help="Description")
@click.pass_context
def new_command(ctx: click.Context, argument: str, option: str) -> None:
    """📝 Brief description.

    Longer description of what this does.

    Examples:
        jira new-command ARG
        jira new-command ARG --option value
    """
    pass
```

### Future Commands (Planned)

- [ ] `jira update` - Update issue fields
- [ ] `jira search` - Search issues with JQL
- [ ] `jira transition` - Change issue status
- [ ] `confluence create` - Create Confluence pages
- [ ] `confluence read` - Read page content
- [ ] `confluence search` - Search Confluence spaces

## 📞 Support

- **Issues**: Report bugs in the GitHub issue tracker
- **Questions**: Ask in the team Slack channel
- **Feedback**: Share improvements and suggestions

## 📄 License

Same as mcp-atlassian-ds project
