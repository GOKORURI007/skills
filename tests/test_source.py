"""source: normalize_source 启发式补全规则。"""

from __future__ import annotations

from skills.source import normalize_source


def test_normalize_owner_repo() -> None:
    """1 个 '/' 当作 GitHub owner/repo → https://github.com/<s>.git"""
    assert normalize_source("op7418/repo") == "https://github.com/op7418/repo.git"
    assert normalize_source("larashero3-dotcom/lieflat-charts") == (
        "https://github.com/larashero3-dotcom/lieflat-charts.git"
    )


def test_normalize_host_path() -> None:
    """≥2 个 '/' 且无 ':' → https://<s>.git（裸 host/owner/repo）"""
    assert normalize_source("github.com/foo/bar") == "https://github.com/foo/bar.git"
    assert normalize_source("gitlab.com/owner/repo/sub") == (
        "https://gitlab.com/owner/repo/sub.git"
    )


def test_normalize_full_url_passthrough() -> None:
    """含 ':' 的完整 URL 原样返回（不补 .git）"""
    assert normalize_source("https://github.com/foo/bar") == "https://github.com/foo/bar"
    assert (
        normalize_source("https://github.com/foo/bar.git") == "https://github.com/foo/bar.git"
    )
    assert (
        normalize_source("git@github.com:foo/bar.git") == "git@github.com:foo/bar.git"
    )


def test_normalize_no_slash_passthrough() -> None:
    """无 '/' 的字符串原样返回（fallback；通常不会到这里）"""
    assert normalize_source("foo") == "foo"
    assert normalize_source("") == ""


def test_normalize_strips_whitespace() -> None:
    assert normalize_source("  op7418/repo  ") == "https://github.com/op7418/repo.git"