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

## Email fallback

- 받는 주소: `coastguard2681@gmail.com`
- 제목: `[{app-id}] 오류 신고 / Bug report`
- 본문 순서: 발생한 문제, 재현 방법, 예상 결과, 앱 정보, 선택적 진단 요약
- GitHub URL과 동일한 앱 메타데이터를 사용하되 사용자가 내용을 수정한 뒤 전송한다.

메일 앱을 열 수 없으면 주소와 본문을 클립보드에 복사하고 사용자에게 알린다.

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
