# errorreport 작업 규칙

이 저장소는 공개 GitHub Issue Form 신고 허브다. `shipping.yml`과 생성기 산출물의 일관성을 우선한다.

## 불변 조건

1. 신고 URL에는 `labels=`나 `body=`를 넣지 않는다. 라벨은 Issue Form YAML의 top-level `labels:`만 사용한다.
2. URL 쿼리 이름은 `template`, `version`, `build`, `os`, `device`, `diagnostics`만 사용하고 폼 필드 ID와 일치시킨다.
3. 전화번호, 이메일, 실명, 사용자 파일 경로, 기기 이름·시리얼, 원본 로그는 자동 입력하지 않는다. `device`는 일반 종류만, `diagnostics`는 200자 이하이며 값을 읽지 못하면 `unknown`을 쓴다.
4. 이메일 신고 경로는 만들거나 되살리지 않는다. 메일 URL 스킴과 신고용 이메일 주소를 코드·문서·UI에 넣지 않는다.
5. 공개 산출물에 비공개 저장소 이름이나 로컬 경로를 넣지 않는다. 특히 `jangbogo`, `restlocktimer`, `ytninza`, `YT-Chita-source-archive`를 노출하지 않는다.
6. `app.id`를 디렉터리명이나 저장소명에서 추론하지 않는다. 반드시 해당 앱의 `shipping.yml`에 명시된 값을 쓴다.
7. GitHub Actions 워크플로를 새로 만들지 않는다.
8. `SECURITY.md`의 비신뢰 입력과 maintainer 승인 게이트를 약화하거나 수정하지 않는다.
9. 아래 로컬 작업 문서는 어떤 저장소에도 커밋하지 않는다.

## ReportKit package

`ReportKit` and `ReportKitUI` are public Swift Package products. The generated
`Sources/ReportKit/ReportTargets.generated.swift` file is produced only by
`uv run python scripts/generate.py` from the approved `shipping.yml` manifests.
Keep the package URL contract aligned with the Issue Form field IDs and never
add `labels` or `body` query parameters.

## 커밋 금지 로컬 문서

- `에러리포트_계획.md`
- `에러리포트_프롬프트.md`
- `GOAL_대개편.md`
- `GOAL_PROGRESS.md`
