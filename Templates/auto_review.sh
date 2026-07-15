#!/bin/bash
# ──────────────────────────────────────────
# SwiftSteps Daily Auto Review
# Codex CLI 기반 자동화 스크립트
# (OpenAI API Key 불필요 — codex login 상태로 동작)
#
# cron 설정:
#   crontab -e
#   0 23 * * * /bin/bash /path/to/auto_review.sh >> /path/to/auto_review.log 2>&1
# ──────────────────────────────────────────

# ✏️ Vault 경로 설정: Templates 폴더의 상위 폴더를 Vault로 사용
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_PATH="$(cd "$SCRIPT_DIR/.." && pwd)"
DAILY_DIR="$VAULT_PATH/Daily"

# 날짜 설정
TODAY=$(date +"%Y-%m-%d")
TOMORROW=$(date -v+1d +"%Y-%m-%d")  # macOS 기준
# Linux라면: TOMORROW=$(date -d "+1 day" +"%Y-%m-%d")

# Daily 노트는 월별 하위 폴더(Daily/YYYY-MM/)에 저장
TODAY_MONTH="${TODAY%-*}"
TOMORROW_MONTH="${TOMORROW%-*}"
TODAY_NOTE="$DAILY_DIR/$TODAY_MONTH/$TODAY.md"
TOMORROW_NOTE="$DAILY_DIR/$TOMORROW_MONTH/$TOMORROW.md"
mkdir -p "$DAILY_DIR/$TODAY_MONTH" "$DAILY_DIR/$TOMORROW_MONTH"

echo ""
echo "🚀 SwiftSteps Daily Review 시작 - $TODAY"
echo "=================================================="

# ──────────────────────────────────────────
# 1. 오늘 노트 존재 확인
# ──────────────────────────────────────────
if [ ! -f "$TODAY_NOTE" ]; then
  echo "❌ 오늘 노트가 없습니다: $TODAY_NOTE"
  echo "   Obsidian에서 오늘 날짜 노트를 먼저 작성해주세요."
  exit 1
fi

echo "📖 오늘 노트 읽기: $TODAY_NOTE"
TODAY_CONTENT=$(cat "$TODAY_NOTE")
TODAY_BEFORE_REVIEW=$(awk '/## 🌙/{exit}1' "$TODAY_NOTE")
NEEDS_NOT_PROGRESS_COMMIT=0

if echo "$TODAY_BEFORE_REVIEW" | grep -qE '^[[:space:]]*-[[:space:]]*\[ \]' || \
   echo "$TODAY_BEFORE_REVIEW" | grep -qE '^[[:space:]]*-[[:space:]]*$'; then
  NEEDS_NOT_PROGRESS_COMMIT=1
fi

# ──────────────────────────────────────────
# 2. Codex CLI로 분석 요청
# ──────────────────────────────────────────
echo "🤖 Codex 분석 중..."

PROMPT="당신은 개발자 학습 코치입니다.
아래는 오늘($TODAY)의 학습 Daily Note입니다.

---
$TODAY_CONTENT
---

다음 작업을 수행해주세요:

1. 오늘 완료된 항목 파악
2. 학습 내용에 대한 전문가 피드백 (2-3문장, 구체적으로)
3. 오늘 배운 개념들의 연결 관계 설명
4. 내일($TOMORROW) 추천 항목 1-2가지 (오늘 미완료 + 다음 단계 반영)
5. 함께 공부하면 좋은 연관 개념 2가지
6. 오늘 배운 핵심 영어 용어

기준:
- 시간대, 이동 시간, 회사 업무는 제외합니다.
- 내일 추천 항목은 작고 실행 가능한 개인 학습 항목만 작성합니다.
- IT 동향만 별도 읽기 자료로 연결할 수 있게 짧게 제안합니다.
- 주식 관련 항목은 사용자가 명시적으로 요청하지 않았다면 내일 할 일이나 읽기 자료로 제안하지 않습니다.

아래 마크다운 형식으로 정확히 출력해주세요:

## 🌙 저녁 회고 (Codex 자동 작성)
> 자동 생성: $TODAY

### ✅ 오늘 완료된 항목
- [완료 항목들]

### 💬 피드백
[피드백 내용]

### 🔗 개념 연결
- [연결 관계]

### 📋 내일 추천 항목
- [ ] [할 것 1]
- [ ] [할 것 2]

### 📚 함께 공부하면 좋은 연관 개념
- [[개념1]]
- [[개념2]]

### 🇺🇸 오늘의 영어 핵심 용어
- \`용어1\`
- \`용어2\`"

TMP_REVIEW=$(mktemp)
TMP_LOG=$(mktemp)

# Codex CLI 실행 (비대화형 모드)
if ! codex exec --ephemeral --sandbox read-only --ask-for-approval never -C "$VAULT_PATH" --output-last-message "$TMP_REVIEW" "$PROMPT" > "$TMP_LOG" 2>&1; then
  echo "❌ Codex 실행에 실패했습니다. codex login 상태와 Codex CLI 설치를 확인해주세요."
  cat "$TMP_LOG"
  rm -f "$TMP_REVIEW" "$TMP_LOG"
  exit 1
fi

REVIEW=$(cat "$TMP_REVIEW")
rm -f "$TMP_REVIEW" "$TMP_LOG"

if [ -z "$REVIEW" ]; then
  echo "❌ Codex 응답을 받지 못했습니다. codex login 상태를 확인해주세요."
  exit 1
fi

# ──────────────────────────────────────────
# 3. 오늘 노트에 저녁 회고 섹션 업데이트
# ──────────────────────────────────────────
echo "✍️  오늘 노트 업데이트 중..."

# 기존 저녁 회고 섹션 제거 후 새 내용 추가
if grep -q "## 🌙 저녁 회고" "$TODAY_NOTE"; then
  # 저녁 회고 섹션 이전 내용만 유지
  BEFORE_REVIEW=$(awk '/## 🌙 저녁 회고/{exit}1' "$TODAY_NOTE")
  echo "$BEFORE_REVIEW" > "$TODAY_NOTE"
fi

# 새 회고 내용 추가
echo "" >> "$TODAY_NOTE"
echo "" >> "$TODAY_NOTE"
echo "$REVIEW" >> "$TODAY_NOTE"

echo "✅ 오늘 노트 업데이트 완료: $TODAY.md"

# ──────────────────────────────────────────
# 3-1. 미완료 상태면 오늘 Daily Note 자동 커밋
# ──────────────────────────────────────────
if [ "$NEEDS_NOT_PROGRESS_COMMIT" -eq 1 ]; then
  echo "🧾 미완료 상태 감지: 진행하지 않음 커밋 확인 중..."
  REL_TODAY_NOTE="Daily/$TODAY_MONTH/$TODAY.md"

  if git -C "$VAULT_PATH" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git -C "$VAULT_PATH" add -- "$REL_TODAY_NOTE"
    if git -C "$VAULT_PATH" diff --cached --quiet -- "$REL_TODAY_NOTE"; then
      echo "ℹ️  커밋할 Daily Note 변경분이 없습니다."
    elif git -C "$VAULT_PATH" commit --only \
      -m "docs(daily): $TODAY 진행하지 않음 기록" \
      -m "체크박스 또는 직접 작성 영역이 미완료라 진행하지 않음을 기록하고 전날 Daily 내용을 보존합니다." \
      -- "$REL_TODAY_NOTE"; then
      echo "✅ 진행하지 않음 자동 커밋 완료: $TODAY"
    else
      echo "⚠️  진행하지 않음 자동 커밋 실패"
    fi
  else
    echo "⚠️  Git 저장소가 아니어서 진행하지 않음 커밋을 건너뜁니다."
  fi
else
  echo "ℹ️  미완료 체크박스/빈 입력 영역이 없어 진행하지 않음 커밋을 생략합니다."
fi

# ──────────────────────────────────────────
# 4. 내일 Daily Note 생성
# ──────────────────────────────────────────
if [ -f "$TOMORROW_NOTE" ]; then
  echo "ℹ️  내일 노트가 이미 존재합니다: $TOMORROW.md"
else
  echo "📄 내일 노트 생성 중..."

  # 내일 추천 항목만 추출 (Codex 응답에서)
  TOMORROW_TASKS=$(echo "$REVIEW" | awk '/### 📋 내일 추천 항목/{found=1; next} found && /^###/{exit} found{print}')
  TOMORROW_YEAR=$(echo "$TOMORROW" | cut -c1-4)

  cat > "$TOMORROW_NOTE" << EOF
# 📅 Daily Note - $TOMORROW

## ✅ 오늘 수행 목록
> 자동 생성 초안. 시간대, 이동 시간, 회사 업무는 넣지 않습니다.

### 필수

$TOMORROW_TASKS

### 짧은 읽기
- [ ] [[Learning/IT Trends/$TOMORROW_YEAR/$TOMORROW - 주제]] 읽기

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
- 제목: [[Learning/IT Trends/$TOMORROW_YEAR/$TOMORROW - 주제]]
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

## 🌙 저녁 회고 (Codex 자동 작성)
> 매일 밤 auto_review.sh가 자동으로 채워줍니다

EOF

  echo "✅ 내일 노트 생성 완료: $TOMORROW.md"
fi

echo "=================================================="
echo "✨ 완료! Obsidian에서 확인해보세요."
echo ""
