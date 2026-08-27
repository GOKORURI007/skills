"""pytest 全局 fixtures。"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def repo_root() -> Path:
    """仓库根：conftest.py 所在 tests/ 目录的父级。"""
    return Path(__file__).resolve().parent.parent