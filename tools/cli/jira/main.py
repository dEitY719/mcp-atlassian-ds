"""Main CLI entry point."""

import logging
import sys

import click

from .commands import jira_group

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# jira_group IS the main entry point
# Just add version option
main = jira_group

# Add version option
main = click.version_option(version="0.1.0")(main)


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
