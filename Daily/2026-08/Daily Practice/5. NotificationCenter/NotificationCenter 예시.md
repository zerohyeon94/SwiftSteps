## ✅ 예제 프로젝트 개요: `SimpleCounter`

### 기능

- **MainViewController**: 숫자 증가 버튼
    
- **LoggerViewController**: 현재 숫자 로그를 실시간 표시
    
- `NotificationCenter`로 두 VC 간 통신

---

## 🧠 실전 팁 요약

| 팁                                                        | 설명  |
| -------------------------------------------------------- | --- |
| `addObserver` → 항상 `deinit`에서 `removeObserver` 처리        |     |
| 여러 VC 또는 Manager → ViewModel 간 통신에 유용                    |     |
| `object:` 매개변수로 특정 객체에서만 발생한 알림 수신 가능                    |     |
| RxSwift에서 Notification을 `.rx.notification(...)` 으로 처리 가능 |     |

---

### 📦 프로젝트 구성 요약

|컴포넌트|설명|
|---|---|
|`MainViewController`|숫자를 증가시키고 `.counterUpdated` Notification을 **post**|
|`LoggerViewController`|`.counterUpdated` Notification을 **수신(addObserver)** 하여 로그 표시|
|`RootTabBarController`|두 VC를 탭바로 묶어 쉽게 화면 전환 가능하게 구성|


---

> [[iOS 학습 인덱스]]