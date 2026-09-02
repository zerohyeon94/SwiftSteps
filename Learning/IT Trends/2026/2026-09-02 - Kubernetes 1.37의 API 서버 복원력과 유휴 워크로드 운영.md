# 2026-09-02 - Kubernetes 1.37의 API 서버 복원력과 유휴 워크로드 운영

> Daily: [[2026-09-02]]
> 분류: IT Trends
> 영역: 클라우드·백엔드·데이터·보안·오픈소스
> 읽기 목표: 5-10분

## 한 줄 요약

Kubernetes 1.37은 API 서버의 watch cache 복원력을 안정화하고, 외부·객체 메트릭 기반 HPA의 0까지 축소를 Beta 기본 기능으로 올리며, `metrics.k8s.io` API를 Stable로 승격했다.

## 왜 지금 볼 만한가

클러스터 업그레이드는 ‘새 기능을 쓸지’만의 문제가 아니다. API 서버가 복구될 때 custom controller가 `429 Too Many Requests`를 제대로 다루는지, 유휴 워크로드가 0개 Pod에서 다시 올라오는 지연을 감당하는지, 자동 확장 도구가 Stable metrics API 전환을 준비했는지까지 운영 계약을 다시 확인하는 일이다.

![[Assets/2026-09-02 - Kubernetes 1.37 - 운영자가 볼 세 가지 변화.svg]]

그림은 이번 릴리스에서 운영자가 우선 볼 세 변화와 점검 지점을 요약한다. 모든 기능이 모든 클러스터에 자동으로 영향을 주는 것은 아니며, feature gate·메트릭 구성·워크로드 설정을 함께 확인해야 한다.

## 핵심 내용

### API 서버: watch cache 복구 때의 요청 폭주를 줄인다

Kubernetes API 서버는 목록 조회와 watch 요청을 watch cache로 처리해 `etcd` 부하를 줄인다. 1.37에서 `WatchCacheInitializationPostStartHook` feature gate가 Stable이 되어, cache 초기화·재초기화 때 비싼 list/watch 요청이 `etcd`에 한꺼번에 몰리는 위험을 줄이는 동작이 완성됐다.

이 변화가 ‘어떤 요청도 실패하지 않는다’는 뜻은 아니다. 과부하 상황에서는 API 서버가 일부 요청을 `429 Too Many Requests`로 거절할 수 있다. custom controller·operator·자동화 스크립트는 이를 서버 장애로만 취급해 즉시 무한 재시도하지 말고, `Retry-After`와 exponential backoff를 존중해야 한다.

### HPA: 조건이 맞으면 0개 Pod까지 축소할 수 있다

1.37에서 HPA scale-to-zero 지원은 Beta로 올라가고 기본 활성화됐다. object 또는 external metric을 사용하는 HPA는 `spec.minReplicas: 0`을 설정해 유휴 시 Pod 수를 0으로 내리고, 수요가 다시 생기면 복원하는 구성을 만들 수 있다. 큐 소비자·배치 작업·GPU 워크로드처럼 유휴 비용이 큰 경우가 대표 후보다.

하지만 `minReplicas: 0`을 넣는다고 모든 워크로드가 자동으로 안전해지는 것은 아니다. 실제로는 메트릭 공급자가 0 상태에서도 수요를 감지할 수 있는지, 첫 요청이 기다릴 수 있는 시간은 얼마인지, 0에서 1로 복원하는 동안의 오류·큐 적체를 어떻게 다룰지를 검증해야 한다. 안정화된 기능과 적절한 서비스 수준은 다른 문제다.

### 메트릭 API: `metrics.k8s.io`가 Stable이 됐다

`metrics.k8s.io` API는 Pod·Node의 CPU·메모리 사용량을 제공하며 `kubectl top`과 HPA의 널리 쓰이는 기반이다. Kubernetes 1.37에서는 이 API가 약 9년의 Beta 기간 뒤 Stable로 승격됐다. Kubernetes 프로젝트는 새 `v1` API를 앞으로의 기준으로 두되, deprecation policy에 맞춰 기존 `v1beta1`도 전환 기간 동안 사용할 수 있다고 설명한다.

따라서 업그레이드 전에는 metrics-server·외부 metrics adapter·사내 dashboard·자동화가 어느 API 버전을 호출하는지 확인하는 편이 좋다. API가 Stable이라는 사실만으로 metric 수집 품질, 권한 설정, HPA 지표의 의미가 자동으로 올바르게 되는 것은 아니다.

## 개발자가 알아둘 변화

1. **컨트롤러 클라이언트**: list/watch 호출에서 429·`Retry-After`·backoff 처리와 idempotent reconcile을 점검한다.
2. **자동 확장 설계**: scale-to-zero 후보에는 메트릭 신호, cold start 시간, 0 상태의 요청 처리 방식을 먼저 적는다.
3. **관측 도구**: `metrics.k8s.io/v1` 전환 계획과 권한·adapter 호환성을 확인한다.
4. **업그레이드 판단**: 릴리스 노트를 기능 목록으로만 읽지 말고, staging 환경에서 API 복구·HPA 복원·기존 자동화의 오류 처리를 함께 확인한다.

## 출처

- [Kubernetes v1.37 release announcement](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/) — watch cache, HPA scale-to-zero, metrics API의 릴리스별 상태와 적용 조건
- [Kubernetes releases](https://kubernetes.io/releases/) — v1.37.0의 2026-08-26 릴리스와 지원 기간
- 출처 확인일: 2026-09-02 (KST)
