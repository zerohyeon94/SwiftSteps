> 간단하게 코드를 작성함에 있어 어떤식으로 작성을 하는지에 대한 예시

## 🔍 프로젝트 개요

이 프로젝트는 **MVVM 아키텍처 기반**으로 다음과 같은 **접근 제어 원칙을 적용**했습니다:

| 구성요소                 | 설명                     | 접근 제어                                    |
| -------------------- | ---------------------- | ---------------------------------------- |
| `UserViewModel`      | API 호출과 데이터 보관         | `private`, `private(set)`, `public func` |
| `APIService`         | Singleton으로 캡슐화        | `final`, `private init()`                |
| `UserViewController` | View 구성 및 ViewModel 호출 | View 전용                                  |

---

## 🎯 핵심 포인트

- ViewModel에서 API 호출은 `public`, 내부 데이터는 `private(set)`
    
- 민감한 인증 토큰은 `private`
    
- 외부에서 데이터를 **읽을 수는 있지만 수정은 불가**

---

## ▶️ 테스트 흐름

1. 앱 실행 시 `UserViewController`가 로드됨
    
2. `viewModel.fetchUser(id:)` 호출
    
3. APIService를 통해 사용자 정보 로드
    
4. 이름/이메일을 레이블에 표시

---

```swift
//
// MVVM + Access Control 예제
// 사용자 정보를 API로 불러오고 접근 제어를 적절히 나눈 구조

import UIKit

// MARK: - 모델
struct UserProfile: Decodable {
    let id: String
    let name: String
    let email: String
}

// MARK: - API Service (Singleton)
final class APIService {
    static let shared = APIService()
    private init() {}

    func fetchUserProfile(userID: String, token: String, completion: @escaping (Result<UserProfile, Error>) -> Void) {
        let url = URL(string: "https://api.example.com/user/\(userID)")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")

        URLSession.shared.dataTask(with: request) { data, _, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            guard let data = data else {
                completion(.failure(NSError(domain: "No Data", code: -1)))
                return
            }
            do {
                let profile = try JSONDecoder().decode(UserProfile.self, from: data)
                completion(.success(profile))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// MARK: - ViewModel
final class UserViewModel {

    // 외부에서 바인딩할 수 있는 output (읽기만 가능)
    private(set) var userName: String? = nil
    private(set) var userEmail: String? = nil

    // 민감 정보는 외부에 노출하지 않음
    private let authToken: String = "top_secret_token"

    // API 호출 함수만 public
    func fetchUser(id: String, completion: @escaping () -> Void) {
        APIService.shared.fetchUserProfile(userID: id, token: authToken) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let user):
                    self?.userName = user.name
                    self?.userEmail = user.email
                case .failure(let error):
                    print("❌ API 실패: \(error.localizedDescription)")
                }
                completion()
            }
        }
    }
}

// MARK: - ViewController
class UserViewController: UIViewController {
    private let nameLabel = UILabel()
    private let emailLabel = UILabel()
    private let viewModel = UserViewModel()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white
        setupUI()
        loadUser()
    }

    private func setupUI() {
        nameLabel.translatesAutoresizingMaskIntoConstraints = false
        emailLabel.translatesAutoresizingMaskIntoConstraints = false
        nameLabel.font = .boldSystemFont(ofSize: 24)
        emailLabel.font = .systemFont(ofSize: 18)

        view.addSubview(nameLabel)
        view.addSubview(emailLabel)

        NSLayoutConstraint.activate([
            nameLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            nameLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 100),

            emailLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            emailLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 20)
        ])
    }

    private func loadUser() {
        viewModel.fetchUser(id: "user123") { [weak self] in
            self?.nameLabel.text = "이름: \(self?.viewModel.userName ?? "-")"
            self?.emailLabel.text = "이메일: \(self?.viewModel.userEmail ?? "-")"
        }
    }
}

```

---

## ✅ 정리 및 피드백

| 항목                                                    | 설명                                                                              | 👍 평가                                |
| ----------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------ |
| `final class APIService`                              | 싱글톤이며 상속 불가능하도록 `final`로 선언                                                     | ✅ 정확합니다                              |
| `fetchUserProfile`의 접근 수준                             | 현재 코드에서는 **`public`**이 아니라 **`internal`** 상태이므로 같은 모듈 내 `UserViewModel`에서 사용 가능 | ✅ 다만 _internal은 기본값_이며, **명시된 건 아님** |
| `authToken`                                           | 민감한 데이터이므로 `private`으로 선언 → 외부 노출 X                                             | ✅ 정확합니다                              |
| `userName`, `userEmail`                               | 외부에서 수정 불가(read-only)를 위해 `private(set)` 사용                                     | ✅ 완벽합니다                              |
| `fetchUser`                                           | ViewController에서 호출해야 하므로 `public` 또는 `internal` → `internal`로 충분 (같은 모듈 내 접근)  | ✅ 정확합니다                              |
| `UserViewController`의 `label`, `viewModel`, `setupUI` | 모두 해당 ViewController 내부 전용이므로 `private` 사용                                      | ✅ 설계 의도 완벽 이해                        |


---

> [[iOS 학습 인덱스]]