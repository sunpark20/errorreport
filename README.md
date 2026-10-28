# App Error Reports

이 저장소는 Sunguk이 배포하는 앱의 공개 버그 신고 창구입니다.
This repository is the public bug-reporting hub for apps published by Sunguk.

## 신고하기 / Report a bug

<!-- BEGIN GENERATED REPORT LINKS -->
- [BIP-0039 Mnemonic 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=bip0039-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [Book 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=book-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [Breaklock Timer 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=breaklock-timer-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [CallNinja - Spam Call Blocker 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=callninja-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [Century Iris 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=centuryiris-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [Earth: World Time & Sky 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=earth-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [The Bird That Drinks Water 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=eatwater-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [Gnomon 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=gnomon-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [LongScreenshot 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=longscreenshot-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [기억의궁전 뇌모닉 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=memory-palace-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [Quick Quit 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=quick-quit-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [SnapCart Grocery Calculator 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=snapcart-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [SpamCall070 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=spamcall070-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [오늘 열었을까 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=todayopen-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [YT Chita 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=yt-bulk-downloader-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
- [YTDI 버그 신고 / Bug report](https://github.com/sunpark20/errorreport/issues/new?template=ytdi-bug.yml&version=unknown&build=unknown&os=unknown&device=unknown&diagnostics=unknown)
<!-- END GENERATED REPORT LINKS -->

앱 안의 **GitHub에 신고 / Report on GitHub** 버튼을 사용하면 앱 버전과 운영체제 정보가 자동으로 채워집니다.
Using the in-app report button pre-fills the app version and operating-system details.

## 공개 범위 / Public visibility

이곳의 이슈와 첨부 파일은 누구나 볼 수 있습니다. 다음 정보는 올리지 마세요.
Issues and attachments here are public. Do not include:

- 전화번호, 이메일 주소 또는 실명 / phone numbers, email addresses, or real names
- 영수증, 계정 정보 또는 API 키 / receipts, account information, or API keys
- 원본 로그, 사용자 파일 경로 또는 기기 식별자 / raw logs, user file paths, or device identifiers

민감정보는 가린 뒤 공개 이슈에 올리거나 App Store 리뷰로 알려 주세요.
Redact sensitive data before filing a public issue, or let us know in an App Store review.

## 처리 방식 / What happens next

신고는 사람이 먼저 확인합니다. 외부 사용자가 작성한 이슈만으로 코드 에이전트나 자동 수정이 실행되지 않습니다.
Every report is reviewed by a person first. User-submitted content never triggers an automated coding agent by itself.

## Swift Package / ReportKit

이 저장소에는 앱에서 공개 GitHub Issue Form을 여는 `ReportKit`과 선택적인 SwiftUI 모듈 `ReportKitUI`가 포함되어 있습니다.
The repository also ships the `ReportKit` Swift package and its optional `ReportKitUI` SwiftUI module.

```swift
import ReportKit

let target = ReportTargets.gnomon
if let link = target.github(metadata: .current()) {
    ReportOpener.open(link)
}
```

매니페스트를 변경한 뒤 모든 공개 산출물을 다시 생성하고 검증합니다.

```sh
SHIPPING_ROOT=/path/to/shipping uv run python scripts/generate.py
SHIPPING_ROOT=/path/to/shipping uv run python scripts/generate.py --check
swift test
```

### Additional source manifests

The generator includes the approved LongScreenshot `shipping.yml` alongside the original 15 shipping apps. Use `--extra-manifest /path/to/shipping.yml` when the source checkout is elsewhere; this option is repeatable. The same manifest set generates the Issue Form, app catalog, labels, README links, and Swift targets. `--check` verifies all of them together.
