# Zero-Alpha-Beta 개요

> [[Home]] > [[Projects/프로젝트 인덱스|Projects]] > Zero-Alpha-Beta
> 태그: #프로젝트 #Electron #ClaudeAPI #AI #TypeScript

---

## 한 줄 설명

"세 개의 인격이 하나의 비서를 이룬다."
macOS 메뉴바 상주 AI 비서 앱 — Zero(ENFJ) · Alpha(INTJ) · Beta(ISFJ)

---

## 프로젝트 경로

```
/Users/joyeonghyeon/Developer/Zero-Alpha-Beta/
```

---

## 기술 스택

| 레이어 | 기술 |
|--------|------|
| 플랫폼 | Electron 34 + electron-vite |
| UI | React 18 + TypeScript |
| AI 엔진 | Claude API (claude-sonnet-4-6) |
| 저장 | electron-store (로컬) |
| 패키징 | electron-builder (.dmg) |

---

## 캐릭터 설계

| 이름    | MBTI | 역할            | 말투            |
| ----- | ---- | ------------- | ------------- |
| Zero  | ENFJ | 사용자 — 비전 제시   | —             |
| Alpha | INTJ | 기술 분석, 논리 검증  | 단호, 짧게, 사족 없음 |
| Beta  | ISFJ | 일정 관리, 감정 서포트 | 친절하고 다정한 존댓말  |

---

## 현재 개발 상태 (Phase 1)

- [x] 프로젝트 초기 세팅 (Electron + Vite + React + TypeScript)
- [x] 컴포넌트 뼈대 (ChatWindow, PersonaSelector, MessageBubble, SettingsPanel)
- [x] 개발 문서 체계 구성 (docs/)
- [ ] Claude API 실제 연동 (Alpha/Beta 시스템 프롬프트)
- [ ] 페르소나 전환 실제 동작
- [ ] 대화 히스토리 로컬 저장

---

## 개발 문서 (프로젝트 내부)

프로젝트 폴더의 `docs/` 에서 관리:
- `docs/개발 일지/` — 날짜별 작업 기록
- `docs/트러블슈팅/` — 문제 → 원인 → 해결
- `docs/아키텍처 결정/` — ADR (Electron 선택, Claude API, 페르소나 분리)
- `docs/기능 개발/` — 페르소나 시스템, 채팅 UI, 메뉴바 트레이
- `docs/개선 방향/` — 백로그 및 아이디어

---

## 학습 연결

이 프로젝트를 통해 연결되는 학습 영역:

| 주제 | 관련 학습 노트 |
|------|---------------|
| Claude API 활용, 페르소나 프롬프트 설계 | [[AI 학습 인덱스]] |
| IPC(프로세스 간 통신), 이벤트 루프 | [[CS 학습 인덱스]] |
| CI/CD (GitHub Actions) | [[CI-CD 개념 정리]] |
| Git 브랜치 전략 | [[Git 병합 전략 - merge vs squash vs rebase]] |

---

> 연결: [[Home]] | [[AI 학습 인덱스]] | [[CS 학습 인덱스]]
