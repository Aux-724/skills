"""Checkout-root resolution for the PPT Master skill package.

Upstream clones and typical ``npx skills`` installs place this package at
``<root>/skills/ppt-master``, so the repository root is two directories above
the skill. This collection places the same package at ``<root>/ppt-master``
and symlinks ``skills/ppt-master`` to it. ``Path.resolve()`` follows that
link, so detection uses the real parent directory name.

Working decks still live in ``<root>/projects``. Documented commands such as
``python3 skills/ppt-master/scripts/project_manager.py`` keep working from
this collection's root because of the symlink.
"""

from __future__ import annotations

from pathlib import Path


def resolve_repo_root(skill_dir: Path) -> Path:
    """Return the checkout that owns ``projects/`` and ``requirements.txt``."""
    if skill_dir.parent.name == "skills":
        return skill_dir.parent.parent
    return skill_dir.parent
