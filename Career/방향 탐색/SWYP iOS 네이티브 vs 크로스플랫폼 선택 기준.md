# SWYP iOS 네이티브 vs 크로스플랫폼 선택 기준

> 연결 Daily: [[2026-05-24]]
> 관련 노트: [[Conversations/Mobile Mentoring/iOS 네이티브 커리어 방향/1. AIOps, AI헬스케어 조교, Swyp 선택 기준]]
> 목적: SWYP 앱서비스를 진행할 때 iOS 네이티브, Flutter, React Native 중 어떤 선택이 현재 커리어 방향에 가장 도움이 되는지 비교한다.

---

## 1. 현재 기준점

지금 기술 선택의 기준은 단순히 `무엇이 더 좋다`가 아니다.

현재 커리어 기준선은 아래에 가깝다.

```text
AI/헬스케어 경험을 이해하고,
교육/콘텐츠화 역량도 있으며,
iOS 앱으로 구현할 수 있는 모바일 개발자
```

따라서 SWYP에서의 기술 선택은 아래 질문으로 판단한다.

```text
이 선택이 6개월 뒤 나를 어떤 개발자로 보이게 하는가?
```

---

## 2. 한 줄 결론

현재 추천은 `iOS 네이티브 우선`이다.

다만 팀 목표가 iOS/Android 동시 출시라면 Flutter 또는 React Native를 검토할 수 있다.

```text
기본 추천:
- iOS 네이티브

크로스플랫폼 검토 조건:
- 팀이 iOS/Android 동시 출시를 요구한다.
- MVP 검증이 iOS 포트폴리오보다 중요하다.
- 팀원이 Flutter 또는 React Native 경험을 이미 갖고 있다.
```

---

## 3. iOS 네이티브 선택

기술 스택 예시:

```text
SwiftUI
Swift Concurrency(async/await)
URLSession 또는 Alamofire
SwiftData 또는 SQLite/Realm
Core ML / Vision / HealthKit 확장 가능성
App Store 배포 경험
```

### 장점

#### 1. 커리어 신호가 가장 선명하다

SWYP 결과물을 이력서에 쓸 때 아래처럼 말할 수 있다.

```text
SwiftUI 기반 iOS 앱서비스를 설계하고 구현했습니다.
API 연동, 상태 관리, 화면 흐름, 배포까지 경험했습니다.
AI/헬스케어 기능으로 확장 가능한 구조를 고려했습니다.
```

이 문장은 현재 꿈인 iOS 네이티브 개발자와 가장 잘 이어진다.

#### 2. Apple 생태계 AI와 직접 연결된다

Apple 공식 문서 기준으로 SwiftUI는 Apple 플랫폼 전반의 UI 프레임워크이고, Core ML은 ML 모델을 앱에 통합하는 공식 경로다.

따라서 SWYP 앱이 당장 AI 기능을 넣지 않더라도, 나중에 아래로 확장하기 쉽다.

```text
Core ML
Vision
HealthKit
Foundation Models
App Intents
on-device AI
```

#### 3. 기존 경험을 가장 잘 살린다

이미 Swift, UIKit, SwiftUI, Kotlin 경험이 있으므로 새 언어/프레임워크 학습 부담이 상대적으로 적다.

현재 넥스트러너스 조교 업무로 Python 학습 부담이 있는 상태에서는, SWYP에서까지 새 프레임워크를 깊게 배우는 것이 부담이 될 수 있다.

#### 4. iOS 품질을 깊게 챙길 수 있다

권한, 알림, 카메라, 위치, 결제, 접근성, App Store 심사, Apple HIG에 맞는 UX 같은 경험은 네이티브로 할 때 더 선명하게 남는다.

### 단점

#### 1. Android를 바로 가져가기 어렵다

iOS 앱만 만들면 Android 사용자는 초기 검증에서 빠질 수 있다.

서비스 성격상 Android 사용자도 반드시 필요하다면 별도 Android 또는 크로스플랫폼 확장이 필요하다.

#### 2. 팀 설득이 필요할 수 있다

SWYP 팀이 빠른 MVP와 양대 플랫폼 출시를 원한다면 iOS 네이티브만으로는 부족해 보일 수 있다.

이 경우에는 `iOS 우선 MVP → 검증 후 Android 확장` 전략을 제안하는 것이 좋다.

#### 3. 서비스 출시 자체가 목표라면 범위가 좁을 수 있다

서비스 실험의 목표가 특정 플랫폼이 아니라 최대한 많은 유저 검증이라면 iOS 네이티브는 초기 범위가 좁다.

---

## 4. Flutter 선택

기술 스택 예시:

```text
Dart
Flutter
Riverpod / Bloc
Dio
GoRouter
Firebase
Platform Channels
```

### 장점

#### 1. iOS/Android 동시 출시가 쉽다

Flutter는 공식적으로 iOS와 Android를 모두 지원하고, 하나의 코드베이스로 여러 플랫폼에 배포하는 방향이 강하다.

SWYP 팀이 빠르게 양대 플랫폼 MVP를 원한다면 Flutter는 현실적인 선택이다.

#### 2. UI 일관성이 좋다

Flutter는 자체 렌더링 방식이라 플랫폼별 UI 차이를 줄이고, 디자이너가 원하는 화면을 비교적 일관되게 구현하기 좋다.

#### 3. Dart는 비교적 구조적인 언어다

Swift/Kotlin 경험이 있다면 Dart는 JavaScript보다 타입과 구조 면에서 익숙하게 느껴질 수 있다.

#### 4. 크로스플랫폼 모바일 역량을 보여줄 수 있다

이력서에서 아래처럼 말할 수 있다.

```text
Flutter로 iOS/Android 동시 MVP를 구현했습니다.
하나의 코드베이스로 제품 검증 속도를 높였습니다.
```

### 단점

#### 1. iOS 네이티브 신호가 약해진다

Flutter 앱을 만들면 모바일 경험은 남지만, Swift/SwiftUI 개발자로서의 신호는 약해진다.

현재 목표가 iOS 네이티브 회복이라면 이 점이 가장 큰 단점이다.

#### 2. Apple 생태계 기능은 한 겹 더 거쳐야 한다

Core ML, Vision, HealthKit, App Intents 같은 Apple 고유 기능을 깊게 쓰려면 결국 네이티브 브릿지나 플러그인을 다뤄야 한다.

#### 3. 새 프레임워크 학습 부담이 생긴다

현재 Python 조교 업무와 병행한다면 Dart/Flutter 상태관리/라우팅/빌드 시스템까지 새로 익혀야 한다.

---

## 5. React Native 선택

기술 스택 예시:

```text
TypeScript
React Native
Expo 또는 bare React Native
React Navigation
TanStack Query
Native Modules
Firebase
```

### 장점

#### 1. React/웹 생태계와 연결된다

팀에 프론트엔드 개발자나 React 경험자가 있다면 협업이 쉽다.

SWYP가 웹 서비스와 함께 가거나, 팀원이 TypeScript/React에 강하다면 React Native는 좋은 선택이 될 수 있다.

#### 2. 하나의 코드베이스로 모바일 MVP를 빠르게 만들 수 있다

React Native 공식 설명처럼 React Native는 JavaScript로 작성하지만 네이티브 UI로 렌더링하는 접근을 취한다.

앱서비스 MVP를 빠르게 만들고 API 연동, 화면 흐름, 상태 관리를 검증하기 좋다.

#### 3. 제품 개발 경험으로는 강하게 남을 수 있다

이력서에서 아래처럼 말할 수 있다.

```text
React Native와 TypeScript로 크로스플랫폼 앱 MVP를 구현했습니다.
웹/모바일 팀과 함께 제품 기능을 빠르게 검증했습니다.
```

### 단점

#### 1. 현재 기술 축과 조금 더 멀다

영현님의 현재 강점은 Swift/Kotlin/Python/헬스케어에 가깝다.

React Native를 선택하면 TypeScript, React, RN 생태계까지 새로 가져가야 한다.

#### 2. 네이티브 모듈에서 다시 iOS 지식이 필요하다

카메라, HealthKit, Core ML, Vision, 푸시, 결제, 백그라운드 작업처럼 플랫폼 기능이 깊어지면 결국 네이티브 지식이 필요하다.

#### 3. 의존성 관리와 환경 이슈가 부담일 수 있다

React Native는 생태계가 크다는 장점이 있지만, 라이브러리/버전/네이티브 빌드 이슈를 같이 관리해야 한다.

---

## 6. 비교표

| 기준 | iOS 네이티브 | Flutter | React Native |
|---|---|---|---|
| 현재 커리어 적합도 | 가장 높음 | 중간 | 중간 |
| iOS 개발자 신호 | 가장 강함 | 약해짐 | 약해짐 |
| iOS/Android 동시 출시 | 약함 | 강함 | 강함 |
| AI/Apple 생태계 확장 | 가장 좋음 | 브릿지 필요 | 네이티브 모듈 필요 |
| 학습 부담 | 가장 낮음 | 중간 | 중간~높음 |
| 팀 협업 적합 | iOS 중심 팀에 좋음 | 모바일 단일팀에 좋음 | 웹/React 팀에 좋음 |
| 포트폴리오 메시지 | iOS 앱 개발자 | 크로스플랫폼 MVP 개발자 | React/TS 기반 앱 개발자 |
| 현재 추천도 | 1순위 | 조건부 2순위 | 조건부 3순위 |

---

## 7. 선택 기준

### iOS 네이티브를 선택한다

아래 중 2개 이상이면 iOS 네이티브가 맞다.

```text
- SWYP를 iOS 포트폴리오로 쓰고 싶다.
- SwiftUI 감각을 회복하고 싶다.
- AI/헬스케어 기능을 Apple 생태계와 연결하고 싶다.
- App Store 배포 경험을 남기고 싶다.
- Android 동시 출시가 필수는 아니다.
```

### Flutter를 선택한다

아래 중 2개 이상이면 Flutter를 검토한다.

```text
- iOS/Android 동시 출시가 중요하다.
- 팀에 네이티브 개발자가 부족하다.
- UI 일관성과 빠른 MVP가 중요하다.
- Dart/Flutter를 배워도 현재 부담이 과하지 않다.
- 서비스 출시 자체가 iOS 포트폴리오보다 중요하다.
```

### React Native를 선택한다

아래 중 2개 이상이면 React Native를 검토한다.

```text
- 팀에 React/TypeScript 경험자가 있다.
- 웹 서비스와 모바일 앱을 같이 가져간다.
- Expo 기반 빠른 MVP가 중요하다.
- 향후 프론트엔드/풀스택 확장도 고려한다.
- 네이티브 기능이 깊지 않은 앱이다.
```

---

## 8. 최종 추천

현재 방향성에서는 SWYP를 한다면 `iOS 네이티브`가 가장 좋다.

이유는 단순하다.

```text
지금 필요한 것은 기술을 넓히는 것이 아니라,
내가 어떤 모바일 개발자인지 선명하게 남기는 것이다.
```

추천 전략:

```text
1. 첫 버전은 iOS 네이티브로 만든다.
2. SwiftUI + async/await + API 연동 + 명확한 화면 구조를 남긴다.
3. AI/헬스케어 기능은 작게라도 연결 가능한 구조를 만든다.
4. Android 요구가 검증되면 그때 Flutter/React Native 또는 Android Native 확장을 검토한다.
```

---

## 9. 이력서 문장 예시

### iOS 네이티브를 선택한 경우

```text
SwiftUI 기반 iOS 앱서비스를 구현하며 API 연동, 화면 상태 관리, 사용자 흐름 설계, 배포 준비를 경험했습니다.
AI/헬스케어 교육 경험을 바탕으로 향후 Core ML/Vision 기반 기능 확장이 가능한 구조를 고려했습니다.
```

### Flutter를 선택한 경우

```text
Flutter 기반 크로스플랫폼 MVP를 구현하며 iOS/Android 동시 출시를 고려한 화면 구조와 API 연동을 설계했습니다.
```

### React Native를 선택한 경우

```text
React Native와 TypeScript 기반으로 모바일 MVP를 구현하며 React 생태계 기반의 빠른 제품 검증과 API 연동을 경험했습니다.
```

---

## 10. 참고한 공식 문서

- Apple SwiftUI: Apple 플랫폼 전반에서 Swift 기반 UI를 만들기 위한 공식 프레임워크
- Apple Core ML: ML 모델을 앱에 통합하는 공식 프레임워크
- Flutter 공식 문서: iOS/Android 등 멀티플랫폼 지원
- React Native 공식 문서: JavaScript/React 기반으로 네이티브 UI를 렌더링하는 앱 프레임워크
