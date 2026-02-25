"""CLI commands package."""

import click

from .jira import jira_group


@click.group()
def cli() -> None:
    """🔧 DS JIRA CLI - Developer-friendly JIRA command-line interface.

    Examples:
        jira create --project PROJ --type Task --summary "Fix API"
        jira read PROJ-123
        jira custom_field get customfield_10201
    """
    pass


# Register command groups
cli.add_command(jira_group, name="jira")

__all__ = ["cli"]
