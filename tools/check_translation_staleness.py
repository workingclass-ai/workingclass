#!/usr/bin/env python3
"""Flag translations that lag behind the canonical README.md.

Walks `git log` for the canonical README.md and each translation, and warns
when a translation has not been touched since its canonical was last updated.

Exit code 0 = all in sync. Exit code 1 = at least one stale translation.

Use `--max-age-days N` to relax the threshold (default 0: a translation is
stale if its last-modified commit is strictly older than the canonical's).

Designed for CI: it shells out to `git`, so the CI checkout must include enough
history (`fetch-depth: 0` in actions/checkout). On shallow clones it falls back
to file mtimes with a warning.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL = REPO_ROOT / "README.md"
TRANSLATIONS = [
    REPO_ROOT / name
    for name in (
        "README.en.md",
        "README.zh-TW.md",
        "README.es.md",
        "README.fr.md",
        "README.pt.md",
        "README.de.md",
    )
]


@dataclass(frozen=True)
class Verdict:
    path: Path
    canonical_ts: datetime
    translation_ts: datetime
    is_stale: bool
    using_mtime_fallback: bool

    def lag_days(self) -> int:
        return (self.canonical_ts - self.translation_ts).days


def _git_last_commit_ts(path: Path) -> datetime | None:
    """Return the author timestamp of the most recent commit touching `path`,
    or None if git has no record (e.g. shallow clone, untracked file)."""
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "log", "-1", "--format=%aI", "--", str(path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None
    line = out.stdout.strip()
    if not line:
        return None
    return datetime.fromisoformat(line)


def _file_mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def check(max_age_days: int = 0) -> list[Verdict]:
    canonical_ts = _git_last_commit_ts(CANONICAL)
    using_mtime = canonical_ts is None
    if using_mtime:
        canonical_ts = _file_mtime(CANONICAL)

    verdicts: list[Verdict] = []
    for translation in TRANSLATIONS:
        if not translation.exists():
            continue
        ts_git = _git_last_commit_ts(translation)
        ts_using_mtime = ts_git is None
        ts: datetime = ts_git if ts_git is not None else _file_mtime(translation)

        # Translation is stale iff canonical is newer than translation by more
        # than `max_age_days`. Using `>` (strict) at threshold 0 means
        # exactly-equal timestamps are considered fresh.
        threshold = timedelta(days=max_age_days)
        is_stale = (canonical_ts - ts) > threshold

        verdicts.append(
            Verdict(
                path=translation,
                canonical_ts=canonical_ts,
                translation_ts=ts,
                is_stale=is_stale,
                using_mtime_fallback=using_mtime or ts_using_mtime,
            )
        )
    return verdicts


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--max-age-days",
        type=int,
        default=0,
        help="grace period: translations may lag canonical by up to N days (default: 0)",
    )
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="suppress the in-sync table, only print stale entries",
    )
    args = ap.parse_args()

    verdicts = check(args.max_age_days)
    stale = [v for v in verdicts if v.is_stale]

    if any(v.using_mtime_fallback for v in verdicts):
        print(
            "[warn] git log not available for some files (shallow clone?) — "
            "using file mtimes; result may be inaccurate.",
            file=sys.stderr,
        )

    if not args.quiet:
        print(
            f"{'translation':<24} {'canonical':<27} {'translation ts':<27} {'lag'}"
        )
        print("-" * 90)
        for v in verdicts:
            print(
                f"{v.path.name:<24} "
                f"{v.canonical_ts.isoformat(timespec='minutes'):<27} "
                f"{v.translation_ts.isoformat(timespec='minutes'):<27} "
                f"{('STALE +' + str(v.lag_days()) + 'd') if v.is_stale else 'ok'}"
            )

    if stale:
        print(
            f"\n✗ {len(stale)} translation(s) lag behind README.md by more than "
            f"{args.max_age_days} day(s).",
            file=sys.stderr,
        )
        print(
            "  When updating README.md, also update each README.<lang>.md or "
            "open a follow-up PR.",
            file=sys.stderr,
        )
        return 1

    if not args.quiet:
        print(f"\n✓ all {len(verdicts)} translation(s) in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
