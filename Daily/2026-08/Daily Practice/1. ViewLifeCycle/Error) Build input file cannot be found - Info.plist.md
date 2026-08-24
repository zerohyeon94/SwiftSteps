## Error Message

```swift
Build input file cannot be found: '/Users/yeonghyeonjo/Documents/Obsidian/SwiftSteps-iOSPractice/ViewLifeCycle/ViewLifeCycle/Info.plist'. Did you forget to declare this file as an output of a script phase or custom build rule which produces it?
```

Xcode에서 빌드 시 필수 파일(여기선 Info.plist)이 존재하지 않아 빌드가 실패했다는 뜻입니다.

## ✅ 요약하자면:

> ❗ Xcode가 `Info.plist` 파일을 **필요한 위치에서 찾지 못해서** 빌드할 수 없다는 오류입니다.

---

## 🔍 에러 발생 원인

이 에러가 발생하는 주요 원인은 다음과 같습니다:

|원인|설명|
|---|---|
|❌ **`Info.plist` 파일이 실제로 해당 경로에 없음**|프로젝트는 파일이 있다고 믿는데, 디스크에는 없음|
|⚠️ **파일은 있지만, Xcode에 추가되지 않음**|실제로는 존재하지만, 프로젝트 내에는 누락됨|
|📍 **Build Settings에서 잘못된 경로 설정**|`Info.plist` 파일 경로 설정이 잘못 지정됨|
|🧪 **사용자 정의 스크립트가 `Info.plist`를 생성한다고 가정함**|하지만 실제로는 생성 안 됨|

---

## ✅ 해결 방법 4단계

### ① 경로에 실제로 파일이 있는지 확인

Finder 또는 터미널에서 해당 경로로 가보세요:

```bash
cd /Users/yeonghyeonjo/Documents/Obsidian/SwiftSteps-iOSPractice/ViewLifeCycle/ViewLifeCycle/ 
ls
```
``

- **없다면 → 파일이 삭제된 것이므로 복원하거나 새로 만들어야 합니다.**
- **있다면 → Xcode에 정상 연결되어 있는지 확인이 필요합니다.**

---

### ② Xcode에서 Info.plist가 프로젝트에 포함되어 있는지 확인

1. Xcode 좌측 Navigator에서 프로젝트 타겟 선택
2. `Build Settings` → `Packaging` 섹션에서 `Info.plist File` 항목 확인
3. 경로가 올바른지, 그리고 실제 파일이 존재하는지 확인 - ‼️ 내가 해당한 에러

예시:

```swift
$(SRCROOT)/ViewLifeCycle/ViewLifeCycle/Info.plist
```

---

### ③ Info.plist 다시 연결 (있는 경우)

- Xcode 좌측 프로젝트 트리에서 Info.plist가 회색이라면 → 누락된 파일
- 마우스 우클릭 → `Delete` (Remove Reference)
- **다시 드래그 & 드롭 또는 `File > Add Files to`로 연결**

---

### ④ Info.plist 새로 만들기 (없는 경우)

1. `File > New > File... > Property List`
2. 이름: `Info.plist`
3. 생성 후 기본 항목 추가 (e.g., `Bundle name`, `Executable file`, etc.)
4. `TARGET > Build Settings > Info.plist File` 경로를 새로 만든 파일 경로로 지정

---

## 🧠 참고: Info.plist의 역할

- 앱 번들 정보 (앱 이름, 버전, 아이콘, 권한 등)를 정의하는 핵심 설정 파일
- 모든 앱과 대부분의 Extension, Framework는 **자기만의 Info.plist**가 필요함

---
## ✅ 마무리 요약

|문제|해결|
|---|---|
|Info.plist 경로에 파일 없음|새로 만들거나 복원|
|파일은 있으나 Xcode에 없음|프로젝트에 파일 추가|
|경로 잘못 지정됨|Build Settings > Info.plist 경로 수정|


---

> [[iOS 학습 인덱스]]