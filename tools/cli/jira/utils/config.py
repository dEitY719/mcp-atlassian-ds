"""Configuration management for JIRA CLI."""

import json
import logging
import os
from typing import Any

logger = logging.getLogger("jira-cli")


class JiraConfig:
    """JIRA connection configuration from environment variables."""

    def __init__(self) -> None:
        """Initialize JIRA configuration from environment variables.

        Authentication: Personal Access Token (JIRA_PERSONAL_TOKEN)
        """
        self.url = os.getenv("JIRA_URL", "")
        self.pat_token = os.getenv("JIRA_PERSONAL_TOKEN", "")
        self.api_version = os.getenv("JIRA_API_VERSION", "2")

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.url:
            logger.error("JIRA_URL environment variable is required")
            return False

        if not self.pat_token:
            logger.error("JIRA_PERSONAL_TOKEN environment variable is required")
            return False

        return True

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary."""
        return {
            "url": self.url,
            "username": self.username,
            "password": "***" if self.password else "",
            "pat_token": "***" if self.pat_token else "",
            "api_version": self.api_version,
        }

    def __repr__(self) -> str:
        """String representation of config."""
        config_dict = self.to_dict()
        return json.dumps(config_dict, indent=2)
