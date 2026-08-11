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

## `shipping.yml` schema v1

```yaml
schema_version: 1
app:
  id: gnomon
  display_name: Gnomon
  platforms: [macos]
  bundle_ids: [com.sunguk.gnomon.Gnomon]
reporting:
  template: gnomon-bug.yml
  locales: [en]
```

`app.id`는 디렉터리명이나 GitHub 저장소명에서 추론하지 않는다. 향후 생성기는 `shipping.yml`이 있는 앱만 수집하며, 공개 산출물에는 로컬 경로나 비공개 저장소 origin을 포함하지 않는다.

## 변경 이력

- v1.1 — 이메일 폴백 제거
