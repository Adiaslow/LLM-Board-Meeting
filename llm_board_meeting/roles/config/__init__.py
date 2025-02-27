# llm_board_meeting/roles/config/__init__.py

"""
Configuration module for board member roles.

This package contains role-specific configurations including:
- Prompt templates for different roles
- Role-specific behavior parameters
- Default configurations for different role types
"""

from llm_board_meeting.roles.config.role_prompts import (
    get_role_prompts,
    format_prompt_template,
)

__all__ = [
    "get_role_prompts",
    "format_prompt_template",
]
