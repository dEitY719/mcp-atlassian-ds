"""JIRA CLI commands."""

import logging
from typing import Any, Optional

import click

from ..utils import JiraConfig, OutputFormatter

logger = logging.getLogger("jira-cli")


def print_config_if_help(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """Print loaded configuration and help when --help is requested."""
    if not value:
        return

    config = JiraConfig()
    click.echo("\n📋 Configuration loaded from .env:", err=True)
    click.echo(f"   JIRA_URL: {config.url if config.url else '❌ NOT SET'}", err=True)
    click.echo(
        f"   JIRA_PERSONAL_TOKEN: {'✅ SET' if config.pat_token else '❌ NOT SET'}",
        err=True,
    )
    click.echo("", err=True)

    # Now show the help text
    click.echo(ctx.get_help())
    ctx.exit()


@click.group(invoke_without_command=True)
@click.option(
    "--help",
    "-h",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=print_config_if_help,
    help="Show this message and exit.",
)
@click.pass_context
def jira_group(ctx: click.Context) -> None:
    """🎯 JIRA operations - create, read, update issues and manage fields.

    Requires environment variables:
        - JIRA_URL: JIRA instance URL
        - JIRA_PERSONAL_TOKEN: Personal Access Token
    """
    import sys

    # Initialize basic logging configuration (needed for DEBUG messages to appear)
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(name)s - %(message)s'
    )

    # Always load config to check environment variables
    config = JiraConfig()

    # Skip validation for --version requests
    if "--version" in sys.argv:
        return

    # Initialize config in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["config"] = config

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
        # Enable DEBUG logging for all relevant loggers
        logging.basicConfig(level=logging.DEBUG, force=True)
        logging.getLogger("mcp-jira").setLevel(logging.DEBUG)
        logging.getLogger("mcp-atlassian").setLevel(logging.DEBUG)
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        from src.mcp_atlassian.jira.client import JiraClient

        # Create JiraClient (uses config from environment)
        client = JiraClient()

        # Prepare issue fields
        fields = {
            "project": {"key": project},
            "summary": summary,
            "issuetype": {"name": type},
        }

        # Add optional fields
        if description:
            fields["description"] = description
        if assignee:
            fields["assignee"] = {"name": assignee}

        # Create the issue using atlassian-python-api
        created_key = client.jira.create_issue(fields=fields)

        if not created_key:
            raise click.ClickException("Failed to create issue - no key returned")

        # Get the created issue details
        issue_data = client.jira.issue(created_key)

        # Format and display the result
        issue_dict = {
            "key": issue_data.get("key"),
            "summary": issue_data.get("fields", {}).get("summary"),
            "type": issue_data.get("fields", {}).get("issuetype", {}).get("name"),
            "status": issue_data.get("fields", {}).get("status", {}).get("name"),
            "url": issue_data.get("self"),
        }

        click.echo(
            OutputFormatter.format(
                {
                    "status": "success",
                    "message": f"Issue created successfully: {created_key}",
                    "issue": issue_dict,
                },
                format_type=format,
            )
        )

    except ImportError as e:
        raise click.ClickException(
            f"Import failed: {str(e)}. Ensure mcp_atlassian is properly installed."
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
        # Enable DEBUG logging for all relevant loggers
        logging.basicConfig(level=logging.DEBUG, force=True)
        logging.getLogger("mcp-jira").setLevel(logging.DEBUG)
        logging.getLogger("mcp-atlassian").setLevel(logging.DEBUG)
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        from src.mcp_atlassian.jira.client import JiraClient

        # Create JiraClient (uses config from environment)
        client = JiraClient()

        # Get the issue from Jira API using atlassian-python-api
        issue_data = client.jira.issue(issue_key)

        if not issue_data:
            raise click.ClickException(f"Issue {issue_key} not found")

        # Format the issue data for output
        issue_dict = {
            "key": issue_data.get("key"),
            "summary": issue_data.get("fields", {}).get("summary"),
            "type": issue_data.get("fields", {}).get("issuetype", {}).get("name"),
            "status": issue_data.get("fields", {}).get("status", {}).get("name"),
            "assignee": issue_data.get("fields", {}).get("assignee", {}).get("displayName"),
            "created": issue_data.get("fields", {}).get("created"),
            "updated": issue_data.get("fields", {}).get("updated"),
            "url": issue_data.get("self"),
        }

        # Add additional fields if requested
        if fields:
            field_list = [f.strip() for f in fields.split(",") if f.strip()]
            issue_dict["requested_fields"] = {
                f: issue_data.get("fields", {}).get(f)
                for f in field_list
            }

        click.echo(
            OutputFormatter.format(
                {
                    "status": "success",
                    "message": f"Issue {issue_key} retrieved successfully",
                    "issue": issue_dict,
                },
                format_type=format,
            )
        )

    except ImportError as e:
        raise click.ClickException(
            f"Import failed: {str(e)}. Ensure mcp_atlassian is properly installed."
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
        # Enable DEBUG logging for all relevant loggers
        logging.basicConfig(level=logging.DEBUG, force=True)
        logging.getLogger("mcp-jira").setLevel(logging.DEBUG)
        logging.getLogger("mcp-atlassian").setLevel(logging.DEBUG)
        logging.getLogger("jira-cli").setLevel(logging.DEBUG)

    config = ctx.obj["config"]

    try:
        from src.mcp_atlassian.jira.client import JiraClient

        # JiraClient will use JiraConfig.from_env() to read environment variables
        client = JiraClient()

        # Get field information from Jira API
        all_fields = client.jira.get_all_fields()
        field_info = next((f for f in all_fields if f.get("id") == field_id), None)

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
    # Configure logging explicitly - must be done before imports
    if verbose:
        # Enable DEBUG logging for all relevant loggers
        logging.basicConfig(level=logging.DEBUG, force=True, format='%(levelname)s - %(name)s - %(message)s')
    else:
        # Ensure basicConfig is called with INFO level even if not verbose
        logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')

    config = ctx.obj["config"]

    try:
        # Import BEFORE setting logger levels to ensure proper initialization
        from src.mcp_atlassian.jira.config import JiraConfig as MCPJiraConfig
        from src.mcp_atlassian.jira.client import JiraClient

        # CRITICAL: Set logger levels to override default WARNING level
        # This must happen AFTER import but BEFORE calling from_env()
        for logger_name in ["mcp-jira", "mcp-atlassian", "mcp-atlassian.jira",
                            "mcp-atlassian.jira.config", "mcp-atlassian.jira.client"]:
            logging.getLogger(logger_name).setLevel(logging.DEBUG if verbose else logging.INFO)

        # Create JiraClient (which calls JiraConfig.from_env())
        client = JiraClient()

        # Get custom fields from Jira API
        fields = client.jira.get_all_custom_fields()

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
