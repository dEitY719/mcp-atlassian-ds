"""Proxy handling utilities for corporate network environments.

This module handles proxy configuration for corporate environments where
Python requests library ignores NO_PROXY and prioritizes HTTP_PROXY,
unlike curl which respects NO_PROXY correctly.

Key Issue:
  - curl: Respects NO_PROXY list, connects directly to .samsungds.net
  - Python requests: Ignores NO_PROXY, uses HTTP_PROXY (routes through proxy)

Solution:
  - For internal services (.samsungds.net), disable proxy environment variables
    to ensure direct connection.
"""

import logging
import os

logger = logging.getLogger("mcp-atlassian")


def disable_proxy_for_internal_services(url: str, service_name: str = "service") -> None:
    """Disable proxy for internal services in corporate proxy environments.

    In corporate environments with forward proxies, Python's requests library
    prioritizes HTTP_PROXY over NO_PROXY settings (unlike curl). This function
    detects internal services (.samsungds.net) and disables proxy to ensure
    direct connection.

    Args:
        url: The service URL to check
        service_name: Name of the service for logging (e.g., "Jira", "Confluence")

    Example:
        >>> disable_proxy_for_internal_services("https://jira.samsungds.net/", "Jira")
        # Disables HTTP_PROXY for direct connection to internal Jira
    """
    # 🔍 DEBUG: Log all input parameters
    logger.info(f"🔍 [PROXY_DEBUG] disable_proxy_for_internal_services() called")
    logger.info(f"   url={url}")
    logger.info(f"   service_name={service_name}")
    logger.info(f"   Before: HTTP_PROXY={os.getenv('HTTP_PROXY', 'NOT_SET')}")

    if url and ".samsungds.net" in url:
        logger.info(f"✅ [PROXY_DEBUG] Detected internal {service_name} service (.samsungds.net)")
        logger.info(f"   Clearing proxy environment variables...")

        # Clear all proxy environment variables
        # This ensures direct connection for internal .samsungds.net services
        os.environ["HTTP_PROXY"] = ""
        os.environ["HTTPS_PROXY"] = ""
        os.environ["http_proxy"] = ""
        os.environ["https_proxy"] = ""

        logger.info(f"✅ [PROXY_DEBUG] After: HTTP_PROXY={os.getenv('HTTP_PROXY', 'NOT_SET')}")
        logger.info(
            f"Detected internal {service_name} service (.samsungds.net). "
            "Disabling proxy for direct connection."
        )
    else:
        logger.info(f"❌ [PROXY_DEBUG] NOT internal service (no .samsungds.net in URL)")
        logger.info(f"   HTTP_PROXY remains: {os.getenv('HTTP_PROXY', 'NOT_SET')}")
