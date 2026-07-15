# Swift · Kotlin 모바일 네이티브 학습 로드맵

> 적용 시작: 2026-07-15 (KST)
> 운영 변경: 2026-07-16부터 평일 이론·주말 코드 실습으로 분리
> 원본: [Notion - Swift · Kotlin 모바일 네이티브 학습 로드맵](https://app.notion.com/p/39de5d4a0bac8046aecec656cbb0d8f3)
> Daily 운영: [[AGENTS]] · 사용자 방향: [[Profile]]

## 핵심 목표

**iOS를 기반으로 Android 네이티브까지 확장한 모바일 엔지니어**를 목표로 한다.

- 주력: Swift·iOS, Kotlin·Android 네이티브
- 차별점: BLE, IoT, 헬스케어, 실시간 데이터, 암호화 경험
- 추후 확장: 모바일 요구사항이 안정된 뒤 Go API와 React 운영 웹 연결
- 현재 개인 학습의 중심: 모바일 네이티브

## 주간 적용 원칙

- Swift 70%·Kotlin 30%를 기본 비중으로 둔다.
- 공통 언어 개념은 같은 워크북에서 비교한다.
- UIKit·SwiftUI와 Android View·Jetpack Compose 같은 플랫폼 종속 주제는 별도의 날에 다룬다.
- 평일에는 이동 환경에 맞춰 이론 설명, 코드 읽기, 실행 결과 예상, 오류 찾기, 언어 차이 설명에 집중한다.
- 코드 입력·컴파일·직접 구현은 주말에 Mac 또는 Windows 개발 환경에서 수행한다.
- Day 번호는 **완료한 평일 이론 워크북 수**를 기준으로 증가한다. 주말 실습 완료 여부는 별도의 주차 상태로 관리한다.
- 평일 워크북이 미완료이면 다음 평일에 같은 Day를 이월한다. 주말 실습 미완료는 평일 이론 진도를 막지 않는다.
- 주말에는 그 주의 모든 주제를 구현하지 않고, 취약하거나 중요한 주제 2~3개만 선택한다.
- 평일에는 [[Templates/Swift Kotlin 비교 학습 워크북]], 주말에는 [[Templates/Swift Kotlin 주말 통합 실습]]을 사용한다.

## 평일 이론 흐름 — 20~40분

1. 이전 개념 또는 오답 한 가지 떠올리기
2. 새로운 개념 설명 읽기·듣기
3. 실행 결과 하나 예상하기
4. 오류 한 곳 찾기 또는 빈칸·코드 순서 문제 풀기
5. Swift와 Kotlin의 차이를 한 문장으로 설명하기
6. 직접 구현이 필요한 내용은 `주말 실습 대기 카드`에 남기기

평일 완료 기준은 다음과 같다.

- 실행 결과 예상 1개
- 오류 찾기 1개
- Swift·Kotlin 차이 1개
- 오늘의 한 줄 요약 1개

코드를 직접 입력하지 않아도 완료할 수 있지만, 답을 수동적으로 듣기만 하지 않고 최소 한 번은 말하거나 짧게 적는다.

## 토요일 코드 실습 — 60~90분

1. 평일 `주말 실습 대기 카드`에서 취약 주제 2~3개 선택
2. 문서를 닫고 핵심 동작과 예상 결과 회상
3. Swift 코드 작성·실행
4. Kotlin 코드 작성·실행
5. 컴파일 오류 또는 예상과 다른 결과 수정
6. 두 언어의 차이와 실무 선택 기준 기록

## 일요일 복습

1. 토요일에 발생한 오류를 다시 설명하고 수정한다.
2. 핵심 코드 하나를 메모 없이 다시 작성한다.
3. 이번 주 Swift·Kotlin 차이 2~3개를 요약한다.
4. 끝내지 못한 실습은 다음 주말 후보로 이월하되 대기 항목을 3개 이하로 유지한다.

## 1단계 — 평일 이론 워크북 84개

### Day 1~28: 언어 기초와 타입 시스템

- 상수와 변수: Swift `let`·`var`, Kotlin `val`·`var`
- 기본 타입과 타입 추론
- 조건문과 반복문
- 함수와 매개변수
- Swift Optional과 Kotlin Nullable Type
- Array·Dictionary와 List·Map
- `struct`, `class`, `data class`
- 프로퍼티와 초기화
- 열거형과 sealed class 기초
- 타입 캐스팅

### Day 29~56: 중급 언어 개념

- Closure와 Lambda, 고차 함수
- `map`, `filter`, `reduce`
- Protocol과 Interface, Extension, Generic
- 접근 제어, 오류 처리와 Result
- 값 타입과 참조 타입
- Swift ARC와 Kotlin/JVM 메모리 개념
- Swift Concurrency와 Kotlin Coroutine
- AsyncSequence·Combine과 Flow·StateFlow

### Day 57~77: 플랫폼 개념

- iOS: 생명주기, UIKit·SwiftUI, 상태 관리, 화면 전환, 네트워크, 저장, MVVM, Combine·async/await
- Android: Activity·Fragment, Jetpack Compose, 상태 관리, ViewModel, Navigation, Coroutine·Flow, Room, DataStore, 권한과 생명주기

### Day 78~84: 종합 복습

- Swift·Kotlin 핵심 개념 종합 문제
- 두 언어 차이 설명과 오류 코드 수정
- 요구사항 기반 짧은 구현
- 비동기 처리 비교
- 취약 개념 목록 작성

## 이후 단계

| 단계 | 권장 기간 | 결과 |
| --- | ---: | --- |
| 2단계 | 28일 | Android Studio·Compose·Coroutine·Flow·Room·Hilt 등 집중 실습 |
| 3단계 | 112일 | IoT·건강 데이터 기록 및 실시간 모니터링 Android 대표 앱 |
| 4단계 | 42일 | 같은 서비스의 SwiftUI 중심 iOS 구현과 플랫폼 비교 |
| 5단계 | 28일 | 테스트·성능·CI/CD·출시·포트폴리오 정리 |

기존 원본의 권장 학습량은 294일·42주 기준이지만, 현재 운영에서는 1단계 84개를 평일 이론 단위로 진행하고 주말 실습을 별도로 배치하므로 달력상 기간은 더 길어질 수 있다. 날짜보다 이론 완료 수와 주말 실습 기록을 기준으로 조정한다.

## 시작점

- 시작일: 2026-07-15
- 평일 이론·주말 실습 분리 시작일: 2026-07-16
- 첫 주제: Swift `let`·`var`와 Kotlin `val`·`var`
- 첫 워크북 경로: `Conversations/Mobile Mentoring/Swift Kotlin 비교 학습/1단계 - 언어 기초와 타입 시스템/1. 상수와 변수.md`
- 첫 멘토링 시작 문장: "Mobile 멘토링을 시작하겠습니다. 질문: Swift의 let·var와 Kotlin의 val·var는 재할당과 객체 내부 변경을 어떻게 다르게 허용하나요?"
- 첫 주말 실습: Day 1 이후 완료한 평일 이론 중 취약한 주제를 최대 3개 골라 하나의 주간 통합 실습 파일로 묶는다.

## 완료 기준

- Swift 핵심 언어 개념을 정확히 설명한다.
- Kotlin 코드를 읽고 직접 작성한다.
- Android 앱을 기획부터 배포까지 구현한다.
- Compose, Coroutine, Flow, Room, Retrofit, Hilt 등의 선택 이유를 설명한다.
- 같은 요구사항을 iOS와 Android에서 어떻게 다르게 구현했는지 설명한다.
- BLE·IoT·헬스케어 경험을 Android까지 확장한 결과를 제시한다.
