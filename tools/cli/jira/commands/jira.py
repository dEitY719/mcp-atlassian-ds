"""JIRA CLI commands."""

import logging
from typing import Any, Optional

import click

from ..utils import JiraConfig, OutputFormatter

logger = logging.getLogger("jira-cli")


@click.group(invoke_without_command=True)
@click.pass_context
def jira_group(ctx: click.Context) -> None:
    """🎯 JIRA operations - create, read, update issues and manage fields.

    Requires environment variables:
        - JIRA_URL: JIRA instance URL
        - JIRA_PERSONAL_TOKEN: Personal Access Token
    """
    import sys

    # Skip validation for --help, --version requests
    if any(flag in sys.argv for flag in ['--help', '-h', '--version']):
        return

    # Initialize config in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["config"] = JiraConfig()

    # Validate config
    if not ctx.obj["config"].validate():
        raise click.ClickException("Invalid JIRA configuration. Check environment variables.")


@jira_group.command(name="create")
@click.option(
    "--project",
    required=True,
    help="Project key (e.g., PROJ, ABC)",
    metavar="KEY",
)
@click.option(
    "--type",
    required=True,
    help="Issue type (e.g., Task, Bug, Story)",
    metavar="TYPE",
)
@click.option(
    "--summary",
    required=True,
    help="Issue summary/title",
    metavar="TEXT",
)
@click.option(
    "--description",
    default="",
    help="Issue description (optional)",
    metavar="TEXT",
)
@click.option(
    "--assignee",
    default="",
    help="Assignee username (optional)",
    metavar="USERNAME",
)
@click.option(
    "--format",
    default="json",
    type=click.Choice(["json", "yaml", "table"]),
    help="Output format (default: json)",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
@click.pass_context
def create_issue(
    ctx: click.Context,
    project: str,
    type: str,
    summary: str,
    description: str,
    assignee: str,
    format: str,
    verbose: bool,
) -> None:
    """📝 Create a new JIRA issue.

    Examples:
        jira create --project PROJ --type Task --summary "Implement API"
        jira create --project ABC --type Bug --summary "Login fails" --description "User cannot login"
        jira create --project PROJ --type Story --summary "Feature" --assignee john.doe --format table
    """
    if verbose:
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        # Import JiraClient here to avoid circular imports
        from src.mcp_atlassian.jira.client import JiraClient

        client = JiraClient(
            url=config.url,
            username=config.username,
            password=config.password,
            pat=config.pat_token,
        )

        # Create issue
        issue_data = {
            "project": {"key": project},
            "issuetype": {"name": type},
            "summary": summary,
        }

        if description:
            issue_data["description"] = description

        if assignee:
            issue_data["assignee"] = {"name": assignee}

        # This would use the actual client method once implemented
        click.echo(
            OutputFormatter.format(
                {
                    "status": "success",
                    "message": f"Issue will be created in {project}",
                    "issue_data": issue_data,
                    "note": "Integration with JiraClient pending",
                },
                format_type=format,
            )
        )

    except ImportError:
        raise click.ClickException(
            "JiraClient import failed. Ensure mcp_atlassian is properly installed."
        )
    except Exception as e:
        raise click.ClickException(f"Failed to create issue: {str(e)}")


@jira_group.command(name="read")
@click.argument("issue_key", metavar="ISSUE_KEY")
@click.option(
    "--format",
    default="json",
    type=click.Choice(["json", "yaml", "table"]),
    help="Output format (default: json)",
)
@click.option(
    "--fields",
    default="",
    help="Comma-separated fields to include (e.g., summary,status,assignee)",
    metavar="FIELDS",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
@click.pass_context
def read_issue(
    ctx: click.Context,
    issue_key: str,
    format: str,
    fields: str,
    verbose: bool,
) -> None:
    """📖 Read a JIRA issue details.

    Examples:
        jira read PROJ-123
        jira read PROJ-123 --format table
        jira read ABC-456 --fields summary,status,assignee
        jira read PROJ-789 --format yaml --verbose
    """
    if verbose:
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        from src.mcp_atlassian.jira.client import JiraClient

        client = JiraClient(
            url=config.url,
            username=config.username,
            password=config.password,
            pat=config.pat_token,
        )

        # Parse fields
        field_list = [f.strip() for f in fields.split(",") if f.strip()]

        click.echo(
            OutputFormatter.format(
                {
                    "status": "success",
                    "message": f"Issue {issue_key} details",
                    "issue_key": issue_key,
                    "requested_fields": field_list or "all",
                    "note": "Integration with JiraClient pending",
                },
                format_type=format,
            )
        )

    except ImportError:
        raise click.ClickException(
            "JiraClient import failed. Ensure mcp_atlassian is properly installed."
        )
    except Exception as e:
        raise click.ClickException(f"Failed to read issue: {str(e)}")


@jira_group.group(name="custom_field")
@click.pass_context
def custom_field_group(ctx: click.Context) -> None:
    """🔧 Custom field operations - manage JIRA custom fields."""
    pass


@custom_field_group.command(name="get")
@click.argument("field_id", metavar="FIELD_ID")
@click.option(
    "--format",
    default="json",
    type=click.Choice(["json", "yaml", "table"]),
    help="Output format (default: json)",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
@click.pass_context
def get_custom_field(
    ctx: click.Context,
    field_id: str,
    format: str,
    verbose: bool,
) -> None:
    """🔍 Get custom field details by ID.

    Queries JIRA API (GET /rest/api/2/field) to retrieve field information.

    Examples:
        jira custom_field get customfield_10201
        jira custom_field get customfield_10203 --format table
        jira custom_field get customfield_11106 --verbose
    """
    if verbose:
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        from src.mcp_atlassian.jira.client import JiraClient
        from src.mcp_atlassian.jira.fields import FieldsMixin

        client = JiraClient(
            url=config.url,
            username=config.username,
            password=config.password,
            pat=config.pat_token,
        )

        # Mix in FieldsMixin to get field operations
        # This is a temporary workaround - ideally JiraClient would inherit FieldsMixin
        field_info = client.get_field_by_id(field_id)

        if field_info:
            click.echo(
                OutputFormatter.format(field_info, format_type=format)
            )
        else:
            raise click.ClickException(
                f"Field {field_id} not found. "
                "Use 'jira custom_field list' to see all available fields."
            )

    except ImportError:
        raise click.ClickException(
            "JiraClient import failed. Ensure mcp_atlassian is properly installed."
        )
    except Exception as e:
        raise click.ClickException(
            f"Failed to get custom field: {str(e)}"
        )


@custom_field_group.command(name="list")
@click.option(
    "--limit",
    default=20,
    type=int,
    help="Limit number of fields (default: 20)",
    metavar="N",
)
@click.option(
    "--format",
    default="json",
    type=click.Choice(["json", "yaml", "table"]),
    help="Output format (default: json)",
)
@click.option(
    "--search",
    default="",
    help="Search fields by name or ID",
    metavar="KEYWORD",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
@click.pass_context
def list_custom_fields(
    ctx: click.Context,
    limit: int,
    format: str,
    search: str,
    verbose: bool,
) -> None:
    """📋 List all custom fields.

    Examples:
        jira custom_field list
        jira custom_field list --limit 50
        jira custom_field list --search epic
        jira custom_field list --format table
    """
    if verbose:
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        from src.mcp_atlassian.jira.client import JiraClient

        client = JiraClient(
            url=config.url,
            username=config.username,
            password=config.password,
            pat=config.pat_token,
        )

        # Get custom fields
        fields = client.get_custom_fields()

        # Filter by search keyword if provided
        if search:
            fields = [
                f
                for f in fields
                if search.lower()
                in f.get("name", "").lower()
                or search.lower() in f.get("id", "").lower()
            ]

        # Limit results
        fields = fields[:limit]

        output_data = {
            "total": len(fields),
            "limit": limit,
            "fields": fields,
        }

        click.echo(
            OutputFormatter.format(output_data, format_type=format)
        )

    except ImportError:
        raise click.ClickException(
            "JiraClient import failed. Ensure mcp_atlassian is properly installed."
        )
    except Exception as e:
        raise click.ClickException(
            f"Failed to list custom fields: {str(e)}"
        )
