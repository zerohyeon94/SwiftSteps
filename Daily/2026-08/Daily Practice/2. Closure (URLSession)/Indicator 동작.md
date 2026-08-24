### 🛠️ Indicator가 동작했다는 것을 시각적으로 보여주기 위해
#### ✅ 해결 전략

1. `URLSession` 응답은 비동기로 오기 때문에,
2. `loadingIndicator.stopAnimating()`을 **바로 하지 않고**,
3. **0.5초 ~ 1초 후에 실행되도록 지연(delay)** 시킵니다.

---

#### 🔧 적용 코드 예시

```swift
URLSession.shared.dataTask(with: url) { data, _, error in
    DispatchQueue.main.asyncAfter(deadline: .now() + 0.7) {  // 0.7초 딜레이
        self.loadingIndicator.stopAnimating()

        if let data = data, let image = UIImage(data: data) {
            completion(image)
        } else {
            print("❌ 이미지 로딩 실패: \(error?.localizedDescription ?? "알 수 없는 오류")")
            completion(nil)
        }
    }
}.resume()
```

## 💡 팁: “응답은 빨리 와도, 보여주는 건 최소한 0.7초 있다가”

이 방식은 사용자가 **로딩 인디케이터의 존재를 인식할 시간**을 줍니다.

---

## 🧠 더 나아가면?

### 옵션 1: 최소 로딩 시간 보장 (응답 시간이 짧아도 최소 0.7초)

```swift
let startTime = Date()

URLSession.shared.dataTask(with: url) { data, _, error in
    let elapsed = Date().timeIntervalSince(startTime)
    let remaining = max(0.7 - elapsed, 0)

    DispatchQueue.main.asyncAfter(deadline: .now() + remaining) {
        self.loadingIndicator.stopAnimating()
        ...
    }
}.resume()
```

> ✅ 네트워크가 _너무 빨라서_ 로딩이 바로 끝나버리는 상황도 방지합니다.

---

## 📌 정리

|방식|설명|
|---|---|
|`DispatchQueue.main.asyncAfter`|일정 시간 후 실행|
|`Date().timeIntervalSince()`|최소 로딩 시간 보장|
|사용자 경험 측면|“로딩이 있다는 인식”을 도와주는 중요한 UX 요소|


---

> [[iOS 학습 인덱스]]