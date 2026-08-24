## 🔍 코드 분석: `UIView.animate(withDuration:)`

```swift
private func showImageWithFadeIn(_ image: UIImage) {
    imageView.image = image
    
    UIView.animate(withDuration: 5) {
        self.imageView.alpha = 1
    }
}
```

---

### 🔹 동작 순서

1. **초기 상태에서 imageView.alpha = 0**  
    → `imageView`는 보이지 않음 (투명)
    
2. **이미지를 설정**  
    → `imageView.image = image`
    
3. **애니메이션 블록 실행**
    - `UIView.animate(withDuration: 5)`는 **5초 동안**
    - `alpha` 값을 **현재 값(0) → 1.0**으로 **점진적으로 증가시킴**
    - 결과적으로 이미지가 **서서히 나타나는(fade-in)** 효과 발생

---

### 🔹 내부 원리

- `UIView.animate`는 **Core Animation 기반의 속성 애니메이션 API**입니다.
- `UIView`의 대부분 속성 (`alpha`, `frame`, `transform`, `backgroundColor` 등)은 **애니메이션 대상**이 될 수 있습니다.
- 애니메이션 블록 내부의 값 변화는 UIKit이 자동으로 **시간에 따라 부드럽게 보간(interpolate)** 해줍니다.

---

### 🎞 시각적으로 보면

|시간|alpha 값|보이는 정도|
|---|---|---|
|0초|0|완전 투명|
|2.5초|0.5|반쯤 보임|
|5초|1|완전 표시됨|

---

### 🧠 시니어 팁

- ✅ `alpha` 외에도 `transform`, `center`, `bounds` 등 애니메이션 가능
    
- ✅ 동시에 여러 속성도 변경 가능:
	```swift
	UIView.animate(withDuration: 0.5) {
	    self.imageView.alpha = 1
	    self.imageView.transform = CGAffineTransform(scaleX: 1.2, y: 1.2)
	}
	```
- ✅ 애니메이션 완료 후 처리하고 싶으면 `completion:` 파라미터 활용
	```swift
	UIView.animate(withDuration: 0.5, animations: {
	    self.imageView.alpha = 1
	}, completion: { finished in
	    print("✅ 애니메이션 완료")
	})
	```

---

## ✅ 요약

| 개념               | 설명                                   |
| ---------------- | ------------------------------------ |
| `UIView.animate` | 뷰의 속성 변화를 시간에 따라 애니메이션 처리            |
| `alpha`          | 0은 투명, 1은 불투명 (0~1 사이 실수값)           |
| 시간               | `withDuration:`을 통해 조절 (ex. 0.3초~5초) |
| fade-in/fade-out | `alpha` 속성 조작으로 간단히 구현 가능            |


---

> [[iOS 학습 인덱스]]