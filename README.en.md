# 🛠️ DS JIRA MCP (Beta)

> An MCP (Model Context Protocol) server that enables LLMs to utilize DS JIRA.
> LLMs can search, create, and update JIRA issues using this MCP.

This project is based on the open-source original repository [mcp-atlassian](https://github.com/sooperset/mcp-atlassian), customized for the Samsung DS JIRA environment with some bug fixes.

## 📌 Overview

An MCP server that enables LLMs to interact with Jira.
You can access the DS Jira real-time server through MCP.

It uses individual authentication information. Therefore, you can access Jira with your **personal Jira account** instead of a shared account.
Most JIRA operations such as issue modification and comment addition can be performed through MCP.

### 🔐 Authentication System

Jira MCP uses an authentication system based on PAT (Personal Access Token).
This system offers the following advantages:

- **User-specific permissions applied** (Accessible Jira Project information)
- **Personalized service provision** (Checking Jira issues assigned to you, writing Jira comments with your account, etc.)

## 🛠 Usage

Register this server in your MCP client (e.g., Roo Code) settings following the guide below, then ask the AI assistant.

### 🔑 How to Issue Jira PAT

1. Click your profile image in the top right of Jira → Profile → Personal access tokens → Create token
2. Enter a token name (anything is fine) → Disable auto-expiration → Create
3. Copy the generated token

---

### 🧩 Roo Code MCP Config Setup

Write the Roo Code MCP config file (`mcp_settings.json`) as follows, and **change only the `<Your Personal Jira PAT>` part to your own.**

```json
{
    "mcpServers": {
        "jira": {
            "url": "http://mcp-servers--mcp-dsjira-prod.khprdpb01.apps.dks.samsungds.net/mcp/",
            "type": "streamable-http",
            "headers": {
                "Authorization": "Token <Your Personal Jira PAT>"
            },
            "disabled": false,
            "alwaysAllow": [
                "jira_search",
                "jira_get_issue",
                "jira_get_all_projects",
                "jira_get_project_issues",
                "jira_get_worklog",
                "jira_get_transitions",
                "jira_search_fields",
                "jira_get_agile_boards",
                "jira_get_board_issues",
                "jira_get_sprints_from_board",
                "jira_get_sprint_issues",
                "jira_get_issue_link_types",
                "jira_get_user_profile"
            ]
        }
    }
}
```

> Note) The `alwaysAllow` field is for setting tools that can be executed automatically without user approval.
> Currently, only Read-only Tools are set to `alwaysAllow`. Please configure according to your situation.

---

### 💬 Usage Examples

You can make the following requests to the AI assistant using MCP:

```
- "Summarize the issues updated in the ABC project over the past week"
- "Check the details and Epic Link of issue PROJ-123"
- "Create a new issue: Project DMSI, Type Task, Summary 'API Improvement'"
- "Change the status of ISSUE-456 to 'In Progress'"
- "Check the changelog of issue BUG-123"
- "Summarize the issues assigned to me"
- "Show all issues in the '26' W4 sprint"
- "Add a comment to ABC-123 with the following content: 'This issue is completed and will be closed.'"
```

---

## 📋 Supported Features

This MCP server provides the following JIRA features.

### 🔍 Search and Query (Read)

| Tool                          | Description                         |
| ----------------------------- | ----------------------------------- |
| `jira_search`                 | Search issues (JQL query supported) |
| `jira_get_issue`              | Get specific issue details          |
| `jira_get_all_projects`       | Get all projects                    |
| `jira_get_project_issues`     | Get issue list by project           |
| `jira_get_worklog`            | Get work log                        |
| `jira_get_transitions`        | Get available status transitions    |
| `jira_search_fields`          | Search fields                       |
| `jira_get_agile_boards`       | Get Agile boards                    |
| `jira_get_board_issues`       | Get issues in a board               |
| `jira_get_sprints_from_board` | Get sprints from a board            |
| `jira_get_sprint_issues`      | Get issues in a sprint              |
| `jira_get_issue_link_types`   | Get issue link types                |
| `jira_get_user_profile`       | Get user profile information        |

### ✏️ Issue Management (Write)

| Tool                    | Description                                      |
| ----------------------- | ------------------------------------------------ |
| `jira_create_issue`     | Create a new issue                               |
| `jira_update_issue`     | Update issue (field modification, status change) |
| `jira_delete_issue`     | Delete issue                                     |
| `jira_add_comment`      | Add comment                                      |
| `jira_transition_issue` | Transition issue status                          |

### 🏃 Sprint Management (Write)

| Tool                 | Description   |
| -------------------- | ------------- |
| `jira_create_sprint` | Create sprint |
| `jira_update_sprint` | Update sprint |

---

## 🧩 DS JIRA Custom Fields

The AI assistant can use the following custom fields in the DS JIRA environment to search and manage issues:

| Field ID            | Field Name             | Usage Example                |
| ------------------- | ---------------------- | ---------------------------- |
| `customfield_10201` | Epic Link              | Search issues linked to Epic |
| `customfield_10203` | Epic Name              | Group issues by Epic name    |
| `customfield_11106` | Start date (WBSGantt)  | Project start schedule       |
| `customfield_11107` | Finish date (WBSGantt) | Project end schedule         |
| `customfield_15221` | Actual start date      | Actual start date            |
| `customfield_15222` | Actual finish date     | Actual completion date       |
| `customfield_10660` | Type                   | Issue type (Milestone, etc.) |
| `customfield_12905` | Milestone              | Milestone information        |
| `customfield_14804` | Target Project         | Target project               |
| `customfield_15316` | Chip Revision          | Chip revision information    |
| `customfield_15500` | 팀명                   | Team name                    |
| `customfield_10733` | Co-workers             | List of collaborators        |
| `customfield_11301` | Watcher List           | List of watchers             |
| `customfield_11884` | CC List                | List of recipients           |
| `customfield_12351` | Group_CC               | Group recipients             |
| `customfield_14826` | Input Data             | Input data                   |
| `customfield_15239` | Closing Notes          | Closing notes                |

> ### You must enter the field name clearly when querying/searching with these fields.
>
> ### An error may occur if a specific field does not exist in the project or cannot be created.

---

## 🧮 JQL Query Examples

You can request mixed JQL queries to the AI assistant:

```
- Specific issue type: "issuetype = Epic AND project = PROJ"
- Sub-issues in Epic: "parent = PROJ-123"
- Search by status: "status = 'In Progress' AND project = PROJ"
- By assignee: "assignee = currentUser()"
- Recently updated: "updated >= -7d AND project = PROJ"
- Bugs only: "issuetype = Bug AND project = PROJ"
- Tasks assigned to me: "assignee = currentUser() AND status != Done"
- By priority: "priority = High AND project = PROJ"
```

---

## 💡 Tips

1. **Use Custom Fields**: If you request "Find only 5 issues where Chip Revision is 'EVT1'", it searches using the `customfield_15316` field.
2. **Date-based Search**: You can request "issues started this month" or "issues with approaching deadlines".
3. **Check Issues Assigned to You**: You can check your personal issue status by requesting "Summarize the issues assigned to me". (Users are distinguished using the PAT they entered.)
4. **Extract Specific Information from Content**: You can extract or summarize content from issue descriptions, comments, etc.
5. **Split Requests**: If you query too many issues at once, the context may overflow or errors may occur on the MCP side. Please split requests into smaller units.

---

## 🆘 Support

If you have any bugs or inquiries, please leave them in the [Issues](https://github.samsungds.net/hahn21-lee/mcp-dsjira/issues) tab or contact Lee Hahn (hahn21.lee).
For technical issues, you may also refer to the original repo [mcp-atlassian](https://github.com/sooperset/mcp-atlassian).

---

## 📚 Notes

1. Jira usage patterns and rules vary significantly by organization. Therefore, there may be tools that do not work depending on each Jira project's Structure.
2. Since this is still a beta version, the service may not be stable 😭. If problems occur, please leave them in the [Issues](https://github.samsungds.net/hahn21-lee/mcp-dsjira/issues) tab, and I will respond as much as possible.
3. S.LSI Jira is currently (as of 2026/1/22) v8.5.5 and does not support PAT-based authentication. Therefore, this MCP that requires individual authentication cannot be used. After the version is upgraded to 10.3.7 on 1/31 and PAT-based authentication becomes available, we plan to review and support MCP.
