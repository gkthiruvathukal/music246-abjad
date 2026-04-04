from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

project = "Composition using Python and Abjad/LilyPond: Life Beyond Notation Software"
author = "George K. Thiruvathukal"
copyright = "2026, George K. Thiruvathukal"


def _detect_release() -> str:
    if value := os.environ.get("SPHINX_RELEASE"):
        return value
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:
        return "dev"


release = _detect_release()
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = ".rst"

html_theme = "sphinx_book_theme"
html_title = project
html_static_path = ["_static"]
html_extra_path = ["CNAME"]
html_theme_options = {
    "repository_url": "https://github.com/gkthiruvathukal/compositions-abjad",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": False,
    "home_page_in_toc": True,
}

latex_elements = {
    "extraclassoptions": "openany,oneside",
}

latex_documents = [
    (
        "index",
        "composition-report.tex",
        project,
        author,
        "manual",
    ),
]
