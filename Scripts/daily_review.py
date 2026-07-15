#!/usr/bin/env python3
"""
SwiftSteps Daily Auto Review System
====================================
매일 밤 자동 실행:
1. 오늘 Daily Note 읽기
2. Codex CLI로 분석
3. 저녁 회고 섹션 자동 작성
4. 내일 Daily Note 자동 생성

Setup:
  codex login
  cp Scripts/.env.example Scripts/.env  # 선택: Vault 경로/모델 지정
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# ─── 설정 ───────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_VAULT_PATH = SCRIPT_DIR.parent

load_env_file(SCRIPT_DIR / ".env")

VAULT_PATH = Path(os.getenv("OBSIDIAN_VAULT_PATH", str(DEFAULT_VAULT_PATH))).expanduser()
CODEX_BIN = os.getenv("CODEX_BIN", "codex")
CODEX_MODEL = os.getenv("CODEX_MODEL", "").strip()

if not VAULT_PATH.exists():
    print(f"❌ OBSIDIAN_VAULT_PATH가 존재하지 않습니다: {VAULT_PATH}")
    sys.exit(1)


# ─── 날짜 유틸 ──────────────────────────────────────────
today = datetime.now().strftime("%Y-%m-%d")
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Daily 노트는 월별 하위 폴더(Daily/YYYY-MM/)에 저장
today_note_path = VAULT_PATH / "Daily" / today[:7] / f"{today}.md"
tomorrow_note_path = VAULT_PATH / "Daily" / tomorrow[:7] / f"{tomorrow}.md"


def read_today_note() -> str:
    if not today_note_path.exists():
        print(f"⚠️  오늘 노트가 없습니다: {today_note_path}")
        sys.exit(1)
    return today_note_path.read_text(encoding="utf-8")


def parse_review_json(text: str) -> dict:
    cleaned = text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


def content_before_evening_review(content: str) -> str:
    for marker in ("## 🌙 저녁 회고", "## 🌙 오늘 하루 피드백"):
        if marker in content:
            return content.split(marker, 1)[0]
    return content


def has_blank_input_section(content: str) -> bool:
    scoped = content_before_evening_review(content)
    section_keywords = [
        "학습 메모",
        "학습 내용",
        "실습/프로젝트 메모",
        "프로젝트 진행 상황",
        "오늘 하루 정리",
        "오늘 배운 개념 연결",
    ]

    for keyword in section_keywords:
        pattern = re.compile(
            rf"^##\s+.*{re.escape(keyword)}.*$\n(?P<body>.*?)(?=^##\s+|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        for match in pattern.finditer(scoped):
            body = match.group("body")
            if re.search(r"(?m)^\s*-\s*$", body):
                return True
    return False


def should_commit_as_not_progressed(content: str) -> bool:
    scoped = content_before_evening_review(content)
    has_unchecked_checkbox = bool(re.search(r"(?m)^\s*-\s*\[ \]", scoped))
    return has_unchecked_checkbox or has_blank_input_section(scoped)


def auto_commit_not_progressed(note_path: Path, note_date: str, should_commit: bool) -> None:
    if not should_commit:
        print("ℹ️  미완료 체크박스/빈 입력 영역이 없어 진행하지 않음 커밋을 생략합니다.")
        return

    repo_check = subprocess.run(
        ["git", "-C", str(VAULT_PATH), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    if repo_check.returncode != 0:
        print("⚠️  Git 저장소가 아니어서 진행하지 않음 커밋을 건너뜁니다.")
        return

    try:
        relative_note_path = note_path.relative_to(VAULT_PATH)
    except ValueError:
        relative_note_path = note_path

    add_result = subprocess.run(
        ["git", "-C", str(VAULT_PATH), "add", "--", str(relative_note_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if add_result.returncode != 0:
        print("⚠️  Daily Note 자동 스테이징 실패:")
        print(add_result.stderr or add_result.stdout)
        return

    diff_result = subprocess.run(
        ["git", "-C", str(VAULT_PATH), "diff", "--cached", "--quiet", "--", str(relative_note_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if diff_result.returncode == 0:
        print("ℹ️  커밋할 Daily Note 변경분이 없어 진행하지 않음 커밋을 생략합니다.")
        return

    commit_result = subprocess.run(
        [
            "git",
            "-C",
            str(VAULT_PATH),
            "commit",
            "--only",
            "-m",
            f"docs(daily): {note_date} 진행하지 않음 기록",
            "-m",
            "체크박스 또는 직접 작성 영역이 미완료라 진행하지 않음을 기록하고 전날 Daily 내용을 보존합니다.",
            "--",
            str(relative_note_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if commit_result.returncode != 0:
        print("⚠️  진행하지 않음 자동 커밋 실패:")
        print(commit_result.stderr or commit_result.stdout)
        return

    print(f"✅ 진행하지 않음 자동 커밋 완료: {note_date}")


def get_review(note_content: str) -> dict:
    prompt = f"""
당신은 개발자의 학습 코치입니다.
아래는 오늘 하루의 학습 노트입니다. 다음 항목을 JSON 형식으로 작성해주세요.

노트 내용:
{note_content}

응답은 반드시 아래 JSON 형식만 출력하세요. 마크다운 코드블록은 쓰지 마세요.
{{
  "completed": ["완료된 항목1", "완료된 항목2"],
  "feedback": ["피드백1", "피드백2"],
  "tomorrow_tasks": ["내일 할 일1", "내일 할 일2"],
  "concept_connections": ["개념 연결 추천1", "개념 연결 추천2"],
  "english_tip": "오늘 학습과 관련된 영어 표현 1가지"
}}

기준:
- 완료 항목: 체크박스 [x] 또는 내용이 작성된 섹션 기준
- 피드백: 잘한 점 1개 + 개선 제안 1개
- 내일 할 일: 오늘 미완료 + 자연스러운 다음 단계. 시간대, 이동 시간, 회사 업무는 제외할 것
- 내일 할 일은 필수 1-2개로 작게 제한하고, IT 동향만 별도 읽기 자료로 연결할 수 있게 제안할 것
- 주식 관련 항목은 사용자가 명시적으로 요청하지 않았다면 내일 할 일이나 읽기 자료로 제안하지 말 것
- 개념 연결: 오늘 학습한 개념과 연결되는 추천 개념
"""

    with tempfile.NamedTemporaryFile("w+", encoding="utf-8", delete=False) as output_file:
        output_path = Path(output_file.name)

    command = [
        CODEX_BIN,
        "exec",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
        "-C",
        str(VAULT_PATH),
        "--output-last-message",
        str(output_path),
    ]

    if CODEX_MODEL:
        command.extend(["-m", CODEX_MODEL])

    command.append(prompt)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )

        if result.returncode != 0:
            print("❌ Codex 실행에 실패했습니다.")
            print(result.stderr or result.stdout)
            sys.exit(result.returncode)

        review_text = output_path.read_text(encoding="utf-8")
        if not review_text.strip():
            print("❌ Codex 응답이 비어 있습니다. codex login 상태를 확인하세요.")
            sys.exit(1)

        return parse_review_json(review_text)
    finally:
        output_path.unlink(missing_ok=True)


def update_evening_review(review: dict) -> None:
    content = today_note_path.read_text(encoding="utf-8")

    completed_str = "\n".join(f"- ✅ {item}" for item in review["completed"]) or "- 기록된 완료 항목 없음"
    feedback_str = "\n".join(f"- {feedback}" for feedback in review["feedback"])
    tomorrow_str = "\n".join(f"- [ ] {task}" for task in review["tomorrow_tasks"])
    connections_str = "\n".join(f"- {connection}" for connection in review["concept_connections"])
    english_str = review.get("english_tip", "")

    new_section = f"""## 🌙 저녁 회고 (Codex 자동 작성 영역)
> 자동 생성: {datetime.now().strftime("%Y-%m-%d %H:%M")}

### 오늘 완료된 항목
{completed_str}

### 피드백
{feedback_str}

### 내일 추천 항목
{tomorrow_str}

### 연결 개념 추천
{connections_str}

### 💬 오늘의 영어 표현
{english_str}
"""

    if "## 🌙 저녁 회고" in content:
        before = content.split("## 🌙 저녁 회고")[0]
        updated = before.rstrip() + "\n\n---\n\n" + new_section
    else:
        updated = content.rstrip() + "\n\n---\n\n" + new_section

    today_note_path.write_text(updated, encoding="utf-8")
    print(f"✅ 오늘 노트 회고 섹션 업데이트 완료: {today_note_path.name}")


def create_tomorrow_note(review: dict) -> None:
    if tomorrow_note_path.exists():
        print(f"ℹ️  내일 노트 이미 존재: {tomorrow_note_path.name}")
        return

    tomorrow_tasks = "\n".join(f"- [ ] {task}" for task in review["tomorrow_tasks"])
    if not tomorrow_tasks:
        tomorrow_tasks = "- [ ] 오늘의 핵심 학습 파일 1개 읽기"
    tomorrow_year = tomorrow[:4]

    content = f"""# 📅 Daily Note - {tomorrow}

## ✅ 오늘 수행 목록
> 자동 생성 초안. 시간대, 이동 시간, 회사 업무는 넣지 않습니다.

### 필수

{tomorrow_tasks}

### 짧은 읽기
- [ ] [[Learning/IT Trends/{tomorrow_year}/{tomorrow} - 주제]] 읽기

### 선택
- [ ] (선택) [[Conversations/.../선택 주제명]] 훑기

### 마무리
- [ ] 오늘 하루 정리 3줄 남기기

---

## 🧑‍🏫 오늘의 멘토링 시작
> 아침에 Codex가 전날 Daily Note를 읽고 Conversations 학습 파일을 생성한 뒤 연결합니다.

- [ ] [분야] 멘토링 수행
  - 학습 파일: [[Conversations/.../1. 주제명]]
  - 시작 문장: "[분야] 멘토링을 시작하겠습니다. 질문: ..."
  - 답변 파일:
  - 상태 판단: 진행 전 / 완료 / 이월

---

## 🎯 오늘의 학습 추천

### [주제]
📁 [[Conversations/.../1. 주제명]]
> 아침에 Codex가 실제 학습 파일을 생성한 뒤 연결합니다.

---

## 🗞️ 오늘의 짧은 읽기

### IT 동향
- 제목: [[Learning/IT Trends/{tomorrow_year}/{tomorrow} - 주제]]
- 한 줄 요약:
- 연결점:

---

## 📚 학습 메모
> 오늘 공부한 개념/기술 (직접 작성)

-

---

## 🧪 실습/프로젝트 메모
> 개인 프로젝트 또는 포트폴리오 관련으로 직접 작성

### [개인 프로젝트명]
- 오늘 한 것:
- 막힌 부분:
- 다음에 할 것:

---

## 📝 오늘 하루 정리
> 오늘 하루를 내 말로 짧게 정리합니다.

-

---

## 🔗 오늘 배운 개념 연결
> 오늘 학습한 것들이 서로 어떻게 연결되는가?

-

---

## 🌙 저녁 회고 (Codex 자동 작성 영역)
> 매일 밤 자동으로 채워집니다

### 오늘 완료된 항목
-

### 피드백
-

### 내일 추천 항목
-

### 연결 개념 추천
-

### 💬 오늘의 영어 표현
-
"""
    tomorrow_note_path.parent.mkdir(parents=True, exist_ok=True)
    tomorrow_note_path.write_text(content, encoding="utf-8")
    print(f"✅ 내일 노트 생성 완료: {tomorrow_note_path.name}")


def main() -> None:
    print(f"\n🔄 SwiftSteps 일일 자동 리뷰 시작 - {today}")
    print("=" * 50)

    print("📖 오늘 노트 읽는 중...")
    note_content = read_today_note()
    needs_not_progressed_commit = should_commit_as_not_progressed(note_content)

    print("🤖 Codex 분석 중...")
    review = get_review(note_content)

    print("✍️  저녁 회고 작성 중...")
    update_evening_review(review)

    print("🧾 미완료 상태 커밋 확인 중...")
    auto_commit_not_progressed(today_note_path, today, needs_not_progressed_commit)

    print("📅 내일 노트 생성 중...")
    create_tomorrow_note(review)

    print("=" * 50)
    print("✨ 완료! Obsidian에서 확인하세요.\n")


if __name__ == "__main__":
    main()
