"""
Local storage helpers for TriFlow (PySide6).

This module persists tasks and budgets to encrypted files on disk.
It uses Fernet symmetric encryption via the :mod:`core.utils` module
to protect user data.  The file names are deliberately simple and
live in the current working directory.  You can modify these paths
to suit your environment.

Functions:
    load_tasks() -> list[dict]
        Load the list of tasks from disk, decrypting them as needed.

    save_tasks(tasks: list[dict]) -> None
        Save a list of task dictionaries to disk, encrypting them.

    load_budgets() -> list[dict]
        Load the list of budgets/expenses from disk, decrypting.

    save_budgets(budgets: list[dict]) -> None
        Save a list of budget dictionaries to disk, encrypting them.

    export_budgets(budgets: list[dict]) -> None
        Export budgets to a plain JSON file for the user.  This file
        is not encrypted and is intended for sharing or archiving.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from core.utils import load_key, encrypt_data, decrypt_data

# Files used to store encrypted payloads
TASKS_FILE = Path("tasks.enc")
BUDGETS_FILE = Path("budgets.enc")


def _read_encrypted(path: Path) -> List[dict]:
    """Read an encrypted JSON list from *path*.

    If the file does not exist, returns an empty list.
    """
    if not path.exists():
        return []
    key = load_key()
    data = path.read_bytes()
    try:
        return decrypt_data(data, key)
    except Exception:
        # If decryption fails, return empty list rather than raising.
        return []


def _write_encrypted(path: Path, records: List[dict]) -> None:
    """Encrypt *records* and write them to *path*.

    Creates parent directories as needed.
    """
    key = load_key()
    enc = encrypt_data(records, key)
    path.write_bytes(enc)


def load_tasks() -> List[dict]:
    """Load the list of tasks from disk.

    Each task is a dictionary with keys: ``id``, ``description``,
    ``completed`` (bool), and ``created_at`` (ISO string).  If no
    tasks file exists, an empty list is returned.
    """
    return _read_encrypted(TASKS_FILE)


def save_tasks(tasks: List[dict]) -> None:
    """Save the list of tasks to disk, encrypting them."""
    _write_encrypted(TASKS_FILE, tasks)


def load_budgets() -> List[dict]:
    """Load the list of budgets/expenses from disk.

    Each expense is a dictionary with keys: ``id``, ``item``, ``amount``,
    and ``date`` (ISO string).  If no budgets file exists, an empty
    list is returned.
    """
    return _read_encrypted(BUDGETS_FILE)


def save_budgets(budgets: List[dict]) -> None:
    """Save the list of budgets/expenses to disk, encrypting them."""
    _write_encrypted(BUDGETS_FILE, budgets)


def export_budgets(budgets: List[dict]) -> None:
    """Export budgets to a plain JSON file ``budgets_export.json``.

    This function writes the given list of budgets to ``budgets_export.json``
    in the current working directory.  It does not perform any
    encryption and will overwrite any existing file.
    """
    export_path = Path("budgets_export.json")
    with export_path.open("w", encoding="utf-8") as f:
        json.dump(budgets, f, indent=2, ensure_ascii=False)