#!/usr/bin/env python3
"""
PPT Master - Project Management Paths

Own the repository and Skill resource roots used by project-management modules.

Usage:
    Import the required path constants from project_management.paths.

Examples:
    from project_management.paths import PROJECTS_ROOT, SCHEMA_DIR

Dependencies:
    repo_layout (standard library only), for checkout-root detection
"""

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from repo_layout import resolve_repo_root  # noqa: E402

PACKAGE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = PACKAGE_DIR.parent
SKILL_DIR = SCRIPTS_DIR.parent
REPO_ROOT = resolve_repo_root(SKILL_DIR)
PROJECTS_ROOT = REPO_ROOT / "projects"
SOURCE_TO_MD_DIR = SCRIPTS_DIR / "source_to_md"
CHARTS_DIR = SKILL_DIR / "templates" / "charts"
SCHEMA_DIR = SKILL_DIR / "templates" / "schemas"
SCAFFOLD_DIR = SKILL_DIR / "templates" / "scaffolds"
