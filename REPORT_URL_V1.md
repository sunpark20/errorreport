# Report URL v1

앱과 중앙 GitHub Issue Form 사이의 플랫폼 독립 계약입니다. Swift Package나 특정 UI 프레임워크가 아니라 이 문서의 URL과 필드 ID가 공통 자산입니다.

## GitHub URL

```text
https://github.com/sunpark20/errorreport/issues/new
?template={template}
&version={version}
&build={build}
&os={os}
&device={device}
&diagnostics={safe-summary}
```

- 모든 값은 UTF-8 percent-encoding한다.
- 앱별 폼의 필드 ID는 `version`, `build`, `os`, `device`, `diagnostics`로 고정한다.
- `labels=`와 `body=` 쿼리는 사용하지 않는다. 라벨은 폼의 top-level `labels`에서 지정한다.
- `diagnostics`는 200자 이하의 비식별 요약만 허용한다.
- 앱 버전이나 OS를 읽지 못하면 빈 문자열 대신 `unknown`을 사용한다.
- 전화번호, 이메일, 사용자 파일 경로, 기기 이름·시리얼, 원본 로그는 자동 입력하지 않는다.

## 비GitHub 사용자

오류 신고는 GitHub Issue Form 한 경로로만 받습니다. GitHub 계정이 필요할 수 있습니다.

App Store 리뷰와 TestFlight 피드백은 개발자가 별도로 확인할 수 있는 보조 감지 채널일 뿐, 사용자를 안내하는 신고 경로가 아닙니다.

## `shipping.yml` schema v2

앱 정보의 유일한 원천은 각 앱 저장소의 `shipping.yml`이다. 생성기는 schema v1을 읽을 수는 있지만,
현재 공개 레지스트리에 등재되는 10개 앱은 모두 아래 schema v2를 사용한다.

```yaml
schema_version: 2
app:
  id: gnomon
  display_name: Gnomon
  display_name_ko: Gnomon
  tagline_ko: "MacBook 조도센서로 외장 모니터 밝기를 자동으로 맞춰줍니다"
  platforms: [macos]
  bundle_ids: [com.sunguk.gnomon.Gnomon]
  min_os: "macOS 15.0+, Apple Silicon"
  version: "1.8.0"
  status: released # released | unreleased | retired
  updated_at: "2026.08"
release:
  macos: https://github.com/sunpark20/gnomon/releases/tag/v1.8.0
web:
  privacy: null
  support: null
reporting:
  template: gnomon-bug.yml
  locales: [en]
```

`store`와 `release`는 플랫폼별 공개 다운로드 URL을 담는 선택 필드다. `store`가 있으면 우선 사용하고,
없으면 같은 플랫폼의 `release`를 사용한다. `release.web`은 제품 소개 등 웹 다운로드 항목으로 별도 노출한다.

schema v2의 공개 필드에서 생성되는 산출물은 다음과 같다.

- Issue Form 10개와 라벨 목록: `reporting`과 앱 표시 이름
- `apps.json`: 이름·한 줄 설명·플랫폼·최소 OS·버전·상태·다운로드·개인정보/지원 URL·신고 URL
- HOMEninja `data/apps.generated.ts`: 위 공개 필드와 동일한 값

`app.id`는 디렉터리명이나 GitHub 저장소명에서 추론하지 않는다. 생성기는 `shipping.yml`이 있는 앱만 수집하며,
공개 산출물에는 로컬 경로나 비공개 저장소 origin을 포함하지 않는다.

## 변경 이력

- v1.1 — 이메일 폴백 제거
- v2.0 — `shipping.yml`을 공개 앱 레지스트리의 단일 원천으로 확장
