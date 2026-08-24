#!/usr/bin/env python3
"""Daily Note와 당일 생성 자료를 작업 단위로 커밋한다.

Daily 피드백이나 다음 날 노트는 생성하지 않는다. 진행 상태는
`## ✅ 오늘 수행 목록`의 체크박스만으로 판단한다.
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


SCRIPT_DIR = Path(__file__).resolve().parent
VAULT_PATH = Path(
    os.getenv("OBSIDIAN_VAULT_PATH", str(SCRIPT_DIR.parent))
).expanduser().resolve()

ALLOWED_LINK_ROOTS = (
    Path("Conversations"),
    Path("Learning/IT Trends"),
    Path("Learning/General Knowledge"),
    Path("Learning/Stock Basics"),
)


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(VAULT_PATH), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def task_section(note_content: str) -> Optional[str]:
    match = re.search(
        r"^## ✅ 오늘 수행 목록\s*$\n(?P<body>.*?)(?=^##\s+|\Z)",
        note_content,
        re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else None


def is_incomplete(note_content: str) -> bool:
    tasks = task_section(note_content)
    if tasks is None:
        return True
    return bool(re.search(r"(?m)^\s*-\s*\[ \]", tasks))


def linked_generated_files(note_content: str) -> list[Path]:
    targets = re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]", note_content)
    linked_paths: set[Path] = set()

    for target in targets:
        relative = Path(target.strip())
        if relative.suffix == "":
            relative = relative.with_suffix(".md")
        if not any(relative.is_relative_to(root) for root in ALLOWED_LINK_ROOTS):
            continue

        candidate = (VAULT_PATH / relative).resolve()
        try:
            candidate.relative_to(VAULT_PATH)
        except ValueError:
            continue
        if candidate.is_file():
            linked_paths.add(candidate.relative_to(VAULT_PATH))

    return sorted(linked_paths)


def commit_daily(note_path: Path, note_date: str) -> None:
    if run_git("rev-parse", "--is-inside-work-tree").returncode != 0:
        print("⚠️  Git 저장소가 아니어서 커밋을 건너뜁니다.")
        return

    note_content = note_path.read_text(encoding="utf-8")
    relative_note = note_path.relative_to(VAULT_PATH)
    commit_paths = [relative_note, *linked_generated_files(note_content)]
    path_args = [str(path) for path in commit_paths]

    add_result = run_git("add", "--", *path_args)
    if add_result.returncode != 0:
        print("❌ Daily 작업 단위 스테이징에 실패했습니다.")
        print(add_result.stderr or add_result.stdout)
        sys.exit(add_result.returncode)

    if run_git("diff", "--cached", "--quiet", "--", *path_args).returncode == 0:
        print("ℹ️  커밋할 Daily 작업 단위 변경이 없습니다.")
        return

    incomplete = is_incomplete(note_content)
    subject = (
        f"docs(daily): {note_date} 진행하지 않음 기록"
        if incomplete
        else f"docs(daily): {note_date} 학습 기록"
    )
    body = (
        "미완료 체크박스가 있어 진행하지 않음을 기록하고, "
        "Daily와 연결된 생성 자료를 함께 보존합니다."
        if incomplete
        else "Daily와 연결된 생성 자료를 학습 작업 단위로 보존합니다."
    )

    commit_result = run_git(
        "commit",
        "--only",
        "-m",
        subject,
        "-m",
        body,
        "--",
        *path_args,
    )
    if commit_result.returncode != 0:
        print("❌ Daily 작업 단위 커밋에 실패했습니다.")
        print(commit_result.stderr or commit_result.stdout)
        sys.exit(commit_result.returncode)

    print(f"✅ Daily 작업 단위 커밋 완료: {note_date}")


def main() -> None:
    note_date = os.getenv("DAILY_NOTE_DATE", datetime.now().strftime("%Y-%m-%d"))
    note_path = VAULT_PATH / "Daily" / note_date[:7] / f"{note_date}.md"

    if not note_path.is_file():
        print(f"⚠️  Daily Note가 없습니다: {note_path}")
        sys.exit(1)

    commit_daily(note_path, note_date)


if __name__ == "__main__":
    main()
