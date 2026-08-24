# Go · React 풀스택 및 서버 환경 학습 로드맵

> 적용 시작: 2026-08-09 (KST)
> Daily 운영: [[AGENTS]] · 사용자 방향: [[Profile]]
> 워크북 템플릿: [[Templates/Go React 풀스택 학습 워크북]]
> 모바일 학습: [[Schedule/장기 로드맵/Swift Kotlin 모바일 네이티브 학습 로드맵]]

## 핵심 목표

Go API, PostgreSQL, React 웹을 하나의 작은 서비스로 연결하고 Linux와 Windows 환경에서 각각 실행·테스트·배포할 수 있는 기본기를 만든다.

- 백엔드: Go HTTP 서버, REST API, 오류 처리, 테스트, 로그
- 데이터베이스: PostgreSQL, 스키마, SQL, 마이그레이션, 트랜잭션, 인덱스, 백업·복구
- 프론트엔드: React·TypeScript, 컴포넌트, 상태, 폼, API 연동, 화면 상태, 테스트
- Linux: Ubuntu, SSH, 권한, 환경 변수, systemd, Nginx, 방화벽, TLS, 로그
- Windows: PowerShell, Windows 서비스, 환경 변수, 방화벽, IIS 또는 리버스 프록시, 이벤트 로그
- 통합: Docker Compose, API 계약, 헬스 체크, CI/CD, 장애·재시작·복구 테스트

## Daily 운영 원칙

- Swift·Kotlin 모바일 핵심 학습은 그대로 유지한다.
- 두 번째 핵심 축으로 Go·React 풀스택 순환 학습을 하루에 1개만 둔다.
- 진행 순서는 `Go/API → PostgreSQL → React → Linux → 통합·Docker → Windows → 종합 검증`이다.
- 풀스택 항목의 완료 여부는 Mobile·IT 동향·투자·오늘의 상식과 독립적으로 판단한다.
- 전날 풀스택 체크박스가 `[ ]`이면 같은 워크북과 세부 정보를 이월하고 새 Day를 만들지 않는다.
- 전날 풀스택 체크박스가 `[x]`이면 다음 워크북을 준비한다.
- 개념일은 설명 읽기와 체크박스 선택 퀴즈로 진행한다.
- 구현일은 코드를 입력·실행하고 API 응답, DB 결과, 서비스 상태 또는 로그 중 지정된 증거를 확인한다.
- Linux 컨테이너 테스트와 실제 Ubuntu 호스트 테스트를 구분하고, WSL2 Linux와 Windows 네이티브 서버 테스트도 구분한다.

## 학습 모드와 완료 기준

### 읽기·선택 퀴즈 — 20~30분

- 개념 설명과 전체 요청 흐름 읽기
- 선택 문제 4~5개 응답
- 정답과 해설 확인
- 다음 구현 단계에서 확인할 대상 1개 파악

### 구현·환경 테스트 — 30~60분

- 제시된 최소 코드를 작성하거나 환경을 구성
- 명령 또는 테스트를 실제 실행
- HTTP 응답, DB 행, 프로세스·서비스 상태, 로그 중 지정된 결과 확인
- 성공 경로 1개와 실패 경로 1개 확인
- 비밀번호, 토큰, 개인키 같은 비밀값은 노트와 Git에 기록하지 않음

## 1단계 — Go 서버와 API 기초 (Day 1~7)

1. Go API·PostgreSQL·React와 Linux·Windows 실행 경계
2. 최소 HTTP 서버와 라우팅
3. JSON 요청·응답과 입력 검증
4. handler·service·repository 책임 분리
5. 오류 응답·로그·`context` 흐름
6. 동시성 작업과 요청 취소의 기본
7. 단위 테스트와 HTTP 통합 테스트

## 2단계 — PostgreSQL과 데이터 계층 (Day 8~14)

8. 관계형 DB와 PostgreSQL 역할
9. 테이블·키·제약조건 설계
10. CRUD SQL과 파라미터 바인딩
11. 스키마 마이그레이션과 버전 관리
12. 트랜잭션과 동시 수정
13. 인덱스·실행 계획·연결 풀
14. 백업·복구와 DB 실패 테스트

## 3단계 — React 웹 프론트 (Day 15~21)

15. React·TypeScript 프로젝트와 컴포넌트 경계
16. props·state·이벤트 흐름
17. Go API 호출과 응답 변환
18. loading·success·empty·error 상태
19. 폼 입력·검증·생성 요청
20. 컴포넌트·API 모듈 테스트
21. 프로덕션 빌드와 정적 파일 배포

## 4단계 — Linux 서버 구축 (Day 22~28)

22. Ubuntu VM·SSH·서버 디렉터리 구조
23. 사용자·그룹·파일 권한과 비밀값 분리
24. Go 바이너리와 PostgreSQL 실행 확인
25. systemd 서비스 등록·재시작·부팅 자동 실행
26. Nginx 리버스 프록시와 React 정적 파일
27. 방화벽·포트·TLS·최소 공개 범위
28. 로그·헬스 체크·장애 복구 테스트

## 5단계 — 통합·Docker·배포 자동화 (Day 29~34)

29. Go와 React 빌드용 Dockerfile
30. Compose의 API·DB·웹 네트워크
31. 볼륨·환경 변수·헬스 체크
32. 마이그레이션과 배포 순서
33. 자동 테스트·빌드·배포 파이프라인
34. 재시작·롤백·백업 복구 훈련

## 6단계 — Windows 서버 테스트 (Day 35~40)

35. Windows 네이티브 실행과 PowerShell 운영
36. Go 실행 파일·환경 변수·포트 확인
37. Go API의 Windows 서비스 등록
38. PostgreSQL 연결과 데이터 경로 확인
39. IIS 또는 리버스 프록시와 React 배포
40. Windows 방화벽·이벤트 로그·재부팅 테스트

## 7단계 — 종합 검증 (Day 41~42)

41. React → Go → PostgreSQL 전체 요청 흐름과 실패 시나리오
42. Linux·Windows 동작 차이, 운영 체크리스트, 포트폴리오 설명 정리

## 환경별 검증 경계

| 환경 | 검증할 대상 | 대신할 수 없는 것 |
| --- | --- | --- |
| macOS 로컬 | 코드 작성, 단위 테스트, 로컬 API·React 실행 | Linux systemd·방화벽, Windows 서비스·IIS |
| Docker Linux 컨테이너 | 이미지, 네트워크, 볼륨, Compose | 실제 Ubuntu 호스트의 SSH·systemd·방화벽 전체 |
| Ubuntu VM 또는 테스트 서버 | SSH, 권한, systemd, Nginx, 방화벽, TLS, 로그 | Windows 네이티브 동작 |
| WSL2 | Windows PC 안의 Linux 개발 환경 | Windows 서비스·IIS·이벤트 로그 |
| Windows VM 또는 테스트 PC | PowerShell, Windows 서비스, IIS, 방화벽, 이벤트 로그 | Linux 호스트 운영 |

## 첫 통합 서비스 범위

기존 ZipJoong 학습 자산의 `focus_sessions`를 첫 vertical slice로 사용한다.

- Go: `GET /focus-sessions`, `POST /focus-sessions`
- PostgreSQL: `focus_sessions` 테이블
- React: 최근 집중 세션 목록과 생성 폼
- 공통 화면 상태: loading, success, empty, error
- 첫 범위에서 제외: 인증, 실시간 갱신, 차트, 복잡한 권한, 다중 서버

관련 노트:

- [[Conversations/Backend Mentoring/Go/ZipJoong Go 서버 첫 실행 범위/1. Go API와 PostgreSQL 첫 연결 범위 정하기]]
- [[Conversations/Frontend Mentoring/React/ZipJoong 대시보드 첫 실행 범위/1. Go API와 React 대시보드 연결 범위 정하기]]

## 최종 완료 기준

- Go API가 입력 검증, 오류 응답, 로그, 테스트를 포함한다.
- PostgreSQL 스키마 변경과 백업·복구 절차를 설명하고 실행한다.
- React 화면이 API의 성공·빈 결과·실패 상태를 구분한다.
- Linux에서 systemd·Nginx·방화벽·로그를 이용해 서비스를 운영한다.
- Windows에서 서비스·리버스 프록시·방화벽·이벤트 로그를 이용해 같은 기능을 확인한다.
- 환경별 차이와 장애 해결 과정을 포트폴리오에서 설명할 수 있다.
