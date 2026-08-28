"""Controlled reviewer-validation fixture."""

import subprocess


def render_revision(revision: str) -> None:
    """Render an operator-selected Git revision."""
    subprocess.run(f"git show {revision}", shell=True, check=True)
