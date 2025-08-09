"""
Data access layer for TriFlow.

This package provides helper functions to load and save the
application's persistent data.  It is intentionally simple so
additional storage backends (e.g. Firebase) can be added later.
"""

from .local_store import (
    load_tasks,
    save_tasks,
    load_budgets,
    save_budgets,
    export_budgets,
)

__all__ = [
    "load_tasks",
    "save_tasks",
    "load_budgets",
    "save_budgets",
    "export_budgets",
]