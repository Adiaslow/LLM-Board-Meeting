# llm_board_meeting/context_management/layer_config.py

"""
Layer Configuration module for the LLM Board Meeting system.

This module defines the configuration and behavior of different context layers
within the context management system. Each layer represents a distinct level
of context persistence and importance, from immediate discussion to long-term
knowledge.

Layer Types:
1. Active Discussion Layer
   - Immediate conversation context
   - High update frequency
   - Limited retention period
   - Maximum token priority

2. Key Points Layer
   - Important insights and decisions
   - Moderate update frequency
   - Medium-term retention
   - Selective promotion/demotion

3. Meeting Framework Layer
   - Structural meeting elements
   - Low update frequency
   - Session-level persistence
   - Framework-specific rules

4. Persistent Knowledge Layer
   - Long-term organizational memory
   - Very low update frequency
   - Indefinite retention
   - Strict promotion criteria

Configuration Parameters:
- Maximum entries per layer
- Token limits per layer
- Retention policies
- Promotion/demotion rules
- Summarization strategies
- Access patterns
- Update frequencies

The module provides:
- Layer-specific configuration templates
- Policy definition interfaces
- Token management strategies
- Content lifecycle rules
- Inter-layer transition logic

Example:
    ```python
    config = LayerConfig(
        layer_type="key_points",
        max_entries=100,
        max_tokens=2000,
        retention_policy={
            "time_based": {"max_age_hours": 24},
            "importance_based": {"min_score": 0.7}
        },
        summarization_policy={
            "trigger": "token_limit",
            "method": "extractive",
            "target_reduction": 0.5
        }
    )
    ```

This module is essential for maintaining an efficient and organized context
hierarchy, ensuring that information flows appropriately between layers while
maintaining relevant constraints and policies.
"""

from dataclasses import dataclass


@dataclass
class LayerConfig:
    """Configuration for a context layer.

    Attributes:
        max_entries: Maximum number of entries to retain.
        max_tokens: Maximum number of tokens to retain.
        retention_policy: Policy for retaining entries (e.g., "time", "importance").
        summarization_policy: Policy for summarizing entries.
    """

    max_entries: int
    max_tokens: int
    retention_policy: str = "importance"
    summarization_policy: str = "recent_first"
