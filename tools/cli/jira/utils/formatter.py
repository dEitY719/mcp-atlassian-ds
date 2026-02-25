"""Output formatters for different output formats."""

import json
import logging
from typing import Any

try:
    import yaml
except ImportError:
    yaml = None

logger = logging.getLogger("jira-cli")


class OutputFormatter:
    """Format output in different formats: json, yaml, table."""

    @staticmethod
    def format(
        data: Any, format_type: str = "json", indent: int = 2
    ) -> str:
        """
        Format data to specified format.

        Args:
            data: Data to format
            format_type: Output format (json, yaml, table)
            indent: Indentation for JSON/YAML

        Returns:
            Formatted string
        """
        if format_type == "json":
            return OutputFormatter._format_json(data, indent)
        elif format_type == "yaml":
            return OutputFormatter._format_yaml(data)
        elif format_type == "table":
            return OutputFormatter._format_table(data)
        else:
            logger.warning(f"Unknown format: {format_type}, defaulting to json")
            return OutputFormatter._format_json(data, indent)

    @staticmethod
    def _format_json(data: Any, indent: int) -> str:
        """Format as JSON."""
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @staticmethod
    def _format_yaml(data: Any) -> str:
        """Format as YAML."""
        if yaml is None:
            logger.warning("PyYAML not installed, falling back to JSON")
            return json.dumps(data, indent=2, ensure_ascii=False)

        return yaml.dump(data, default_flow_style=False, allow_unicode=True)

    @staticmethod
    def _format_table(data: Any) -> str:
        """Format as table."""
        if isinstance(data, dict):
            if "fields" in data:
                # For field listing
                return OutputFormatter._format_field_table(data.get("fields", []))
            elif "key" in data:
                # For single issue
                return OutputFormatter._format_issue_table(data)
            else:
                # Fallback to JSON for complex structures
                return json.dumps(data, indent=2, ensure_ascii=False)

        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                # For list of items
                return OutputFormatter._format_list_table(data)
            else:
                return json.dumps(data, indent=2, ensure_ascii=False)

        return str(data)

    @staticmethod
    def _format_field_table(fields: list[dict[str, Any]]) -> str:
        """Format fields as table."""
        if not fields:
            return "No fields found."

        lines = []
        lines.append("ID                    | Name                        | Type")
        lines.append("-" * 75)

        for field in fields:
            field_id = field.get("id", "")[:20]
            name = str(field.get("name", ""))[:27]
            field_type = field.get("schema", {}).get("type", "unknown")[:15]

            lines.append(
                f"{field_id:<20} | {name:<27} | {field_type:<15}"
            )

        return "\n".join(lines)

    @staticmethod
    def _format_issue_table(issue: dict[str, Any]) -> str:
        """Format single issue as table."""
        lines = []
        lines.append(f"Issue Key: {issue.get('key', 'N/A')}")
        lines.append(f"Type:      {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
        lines.append(f"Status:    {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
        lines.append(
            f"Summary:   {issue.get('fields', {}).get('summary', 'N/A')}"
        )
        lines.append(
            f"Assignee:  {issue.get('fields', {}).get('assignee', {}).get('displayName', 'Unassigned')}"
        )

        return "\n".join(lines)

    @staticmethod
    def _format_list_table(items: list[dict[str, Any]]) -> str:
        """Format list of items as table."""
        if not items:
            return "No items found."

        # Determine columns from first item
        first_item = items[0]
        columns = list(first_item.keys())[:5]  # Limit to 5 columns

        # Calculate column widths
        col_widths = {}
        for col in columns:
            max_width = max(
                len(col),
                max(
                    len(str(item.get(col, "")))
                    for item in items
                ),
            )
            col_widths[col] = min(max_width, 30)  # Cap at 30 chars

        # Build header
        lines = []
        header = " | ".join(
            col.ljust(col_widths[col]) for col in columns
        )
        lines.append(header)
        lines.append("-" * len(header))

        # Build rows
        for item in items:
            row = " | ".join(
                str(item.get(col, "")).ljust(col_widths[col])
                for col in columns
            )
            lines.append(row)

        return "\n".join(lines)
