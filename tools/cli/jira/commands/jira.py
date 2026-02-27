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
        # Import JiraClient here to avoid circular imports
        from src.mcp_atlassian.jira.client import JiraClient

        # JiraClient will use JiraConfig.from_env() to read environment variables
        # which were loaded from .env file by JiraConfig.__init__
        client = JiraClient()

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
        click.echo("=== CLI DEBUG: Creating JiraClient ===", err=True)
        client = JiraClient()

        # DEBUG: Check client configuration and session headers
        click.echo(f"CLI DEBUG: client.config.url = {client.config.url}", err=True)
        click.echo(f"CLI DEBUG: client.config.auth_type = {client.config.auth_type}", err=True)
        click.echo(f"CLI DEBUG: Session headers = {dict(client.jira._session.headers)}", err=True)
        click.echo("=== CLI DEBUG: END CONFIG CHECK ===\n", err=True)

        # Get custom fields from Jira API
        click.echo("CLI DEBUG: Calling client.jira.get_all_custom_fields()...", err=True)
        fields = client.jira.get_all_custom_fields()
        click.echo(f"CLI DEBUG: Got {len(fields)} fields from API\n", err=True)

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
