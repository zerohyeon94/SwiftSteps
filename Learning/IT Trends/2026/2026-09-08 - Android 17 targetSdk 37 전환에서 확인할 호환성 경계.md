# 2026-09-08 - Android 17 targetSdk 37 전환에서 확인할 호환성 경계

> Daily: [[2026-09-08]]
> 분류: IT Trends
> 영역: 모바일 플랫폼·On-device AI
> 읽기 목표: 5-10분

## 한 줄 요약

Android 17(API level 37)은 target SDK를 올린 앱에 큰 화면 리사이즈, private API·리플렉션, 백그라운드 오디오, Bluetooth RFCOMM 읽기처럼 기존 코드의 가정을 다시 검증해야 하는 행동 변화를 묶어 둔다.

## 왜 지금 볼 만한가

플랫폼 전환에서 `compileSdk` 업데이트와 실제 호환성 확보는 다른 일이다. Android 17은 특히 큰 화면에서 방향·비율 제약을 더 이상 피할 수 없게 하고, reflection·JNI·백그라운드 작업처럼 평소 테스트에서 비어 있는 경로를 드러낸다. iOS 중심 경험을 Android 네이티브로 넓힐 때도 “화면·수명·플랫폼 계약”을 코드 조각이 아니라 사용자 흐름으로 시험하는 습관이 중요하다.

![[Assets/2026-09-08 - Android 17 - targetSdk 37 호환성 경계.svg]]

그림은 공식 문서에서 target SDK 37에 직접 연결한 네 점검 축을 요약한다. 각 변화의 적용 조건과 세부 예외는 앱의 target SDK, 기기 크기, 권한, 라이브러리 버전에 따라 달라질 수 있으므로 원문을 함께 확인한다.

## 핵심 내용

### 큰 화면: 방향 고정과 비율 제한을 설계로 바꾼다

Android 17을 target으로 하는 앱은 `sw >= 600dp` 큰 화면에서 orientation, resizability, aspect ratio 제한을 앱이 계속 강제할 수 없다. Android 16에서 있던 opt-out은 API 37에서 사라진다. 따라서 “세로 화면으로만 보이면 된다”는 전제 대신 창 크기 변화, 분할 화면, 외부 디스플레이에서 상태와 레이아웃이 어떻게 복원되는지 확인해야 한다.

### private 구현 의존: 동작은 같아 보여도 실패 경로가 바뀐다

API 37에서는 `MessageQueue`가 lock-free 구현으로 바뀌며 private 필드·메서드를 reflection으로 보던 코드는 깨질 수 있다. 또 `static final` 필드를 reflection으로 바꾸려 하면 `IllegalAccessException`이 나고, JNI의 `SetStatic<Type>Field` 계열로 바꾸려 하면 앱이 crash할 수 있다. 해결 방향은 private 구현에 의존한 테스트·라이브러리를 공개 SDK/NDK API로 바꾸고, 실제 target 37 환경에서 오류 로그를 보는 것이다.

### 백그라운드 오디오와 화면 내용: “켜져 있다”는 이유만으로 허용되지 않는다

백그라운드에서 재생·audio focus·볼륨 변경을 수행하는 앱은 target 37에서 더 엄격한 조건을 받는다. 공식 문서는 background audio를 하려면 foreground service와 추가 조건을 요구한다고 설명한다. 한편 Content Capture를 끄려고 쓰던 API는 더는 목표를 달성하지 못할 수 있어, 실제 화면 보호가 필요한 경우 `FLAG_SECURE` 같은 의도를 맞는 수단으로 옮겨야 한다.

### 연결성: RFCOMM 읽기 루프의 종료 신호

Bluetooth RFCOMM 소켓에서 얻은 `InputStream.read()`는 Android 17 target 앱에서 소켓 종료·연결 끊김 때 `-1`을 반환한다. 예외만 기다리던 루프는 `-1` 종료를 명시적으로 처리해야 한다. 이 변화는 BLE/IoT 연결에서 재연결 정책과 UI 상태를 분리하는 좋은 점검 지점이다.

## 개발자가 알아둘 변화

1. **호환성 먼저**: target SDK를 올리기 전 현재 앱을 Android 17 기기/에뮬레이터에서 테스트하고, all-app behavior change와 target-specific change를 나눠 읽는다.
2. **큰 화면 시나리오화**: 회전·리사이즈·분할 화면·외부 디스플레이에서 입력 상태, navigation back stack, 미디어·카메라 흐름을 확인한다.
3. **의존성 점검**: reflection·JNI·오래된 SDK가 private API를 만지는지 lint, logcat, 라이브러리 릴리스 노트로 찾는다.
4. **수명 경계 점검**: foreground service, audio, Bluetooth read loop를 lifecycle·권한·취소 흐름과 함께 테스트한다.

## 용어와 맥락

- **target SDK**: 앱이 특정 Android 버전의 행동 변경을 따르겠다고 선언하는 기준이다. 기기에서 실행되는 OS 버전과 같은 뜻은 아니다.
- **`sw >= 600dp`**: 화면의 smallest width가 600dp 이상인 큰 화면 조건이다. 태블릿·폴더블·데스크톱 창 모드가 대표적인 점검 대상이다.
- **RFCOMM**: Bluetooth Classic에서 직렬 포트처럼 데이터를 주고받는 연결 방식이다.

## 출처

- [Android Developers · Android 17 behavior changes](https://developer.android.com/about/versions/17/behavior-changes-17) — target 37에 적용되는 큰 화면·런타임·오디오·Bluetooth 변경
- [Android Developers · Android 17 migration guide](https://developer.android.com/about/versions/17/migration) — 호환성 테스트와 target SDK 전환 순서
- [Android Developers Blog · Android 17 is here](https://developer.android.com/blog/posts/android-17-is-here) — API level 37 릴리스와 플랫폼 전환 배경
- 출처 확인일: 2026-09-08 (KST)
