"""Main CLI entry point."""

import logging
import sys
from typing import Any

import click

from .commands import cli

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0")
def main(ctx: click.Context) -> None:
    """🔧 DS JIRA CLI - Developer-friendly command-line interface.

    Interact with JIRA instances from the command line. Supports creating issues,
    reading issue details, and managing custom fields.

    Setup:
        Set environment variables:
            export JIRA_URL="https://jira.example.com"
            export JIRA_PAT="your_personal_access_token"

            OR for basic auth:
            export JIRA_USERNAME="your_username"
            export JIRA_PASSWORD="your_password"

    Quick Start:
        jira create --project PROJ --type Task --summary "Your task"
        jira read PROJ-123
        jira custom_field get customfield_10201
        jira custom_field list

    Learn more:
        jira --help
        jira jira --help
        jira jira create --help
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Add the jira command group
main.add_command(cli)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        click.echo("\n❌ Interrupted by user", err=True)
        sys.exit(1)
    except click.ClickException as e:
        click.echo(f"❌ Error: {e.message}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        sys.exit(1)
