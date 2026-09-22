#!/usr/bin/env python3
"""Generate the public error-report artifacts and ReportKit catalog."""

from __future__ import annotations

import argparse
import json
import re
from urllib.parse import urlencode
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SHIPPING_ROOT = REPOSITORY_ROOT.parent.parent / "0.shipping"
DEFAULT_SWIFT_OUTPUT = REPOSITORY_ROOT / "Sources" / "ReportKit" / "ReportTargets.generated.swift"
ISSUE_URL = "https://github.com/sunpark20/errorreport/issues/new"
EXPECTED_APP_IDS = frozenset(
    {
        "book",
        "breaklock-timer",
        "callninja",
        "centuryiris",
        "earth",
        "eatwater",
        "gnomon",
        "memory-palace",
        "quick-quit",
        "snapcart",
        "spamcall070",
        "yt-bulk-downloader",
        "ytdi",
    }
)
COMMON_LABELS = (
    "source:appstore",
    "source:github",
    "status:needs-triage",
    "type:bug",
)
VALID_PLATFORMS = frozenset({"android", "ios", "macos", "web", "windows"})
VALID_STATUSES = frozenset({"released", "retired", "unreleased"})
PRIVATE_MARKERS = ("jangbogo", "restlocktimer", "ytninza", "YT-Chita-source-archive")
SWIFT_KEYWORDS = {
    "associatedtype", "class", "deinit", "enum", "extension", "fileprivate",
    "func", "import", "init", "inout", "internal", "let", "open", "operator",
    "private", "protocol", "public", "rethrows", "static", "struct", "subscript",
    "typealias", "var", "break", "case", "continue", "default", "defer", "do",
    "else", "fallthrough", "for", "guard", "if", "in", "repeat", "return",
    "switch", "where", "while", "as", "catch", "false", "is", "nil", "super",
    "self", "Self", "throw", "throws", "true", "try", "_",
}
README_SECTION = re.compile(
    r"(## 신고하기 / Report a bug\n).*?(?=\n## 공개 범위 / Public visibility)",
    re.DOTALL,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--shipping-root",
        type=Path,
        default=DEFAULT_SHIPPING_ROOT,
        help="directory containing one shipping.yml per app",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated artifacts are current without writing them",
    )
    parser.add_argument(
        "--swift-output",
        type=Path,
        default=DEFAULT_SWIFT_OUTPUT,
        help="generated ReportKit Swift catalog path",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    raise SystemExit(f"generate.py: {message}")


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail(f"{label} must be a mapping")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value.strip()


def optional_string(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return require_string(value, label)


def require_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        fail(f"{label} must be a non-empty list")
    return [require_string(item, f"{label} item") for item in value]


def public_urls(value: Any, label: str) -> dict[str, str]:
    if value is None:
        return {}
    urls = require_mapping(value, label)
    result: dict[str, str] = {}
    for platform, url in urls.items():
        if platform not in VALID_PLATFORMS:
            fail(f"{label}.{platform} is not a supported platform")
        normalized = optional_string(url, f"{label}.{platform}")
        if normalized is not None:
            result[platform] = normalized
    return result


def load_apps(shipping_root: Path) -> list[dict[str, Any]]:
    manifests = sorted(shipping_root.glob("*/shipping.yml"))
    if len(manifests) != len(EXPECTED_APP_IDS):
        fail(f"expected {len(EXPECTED_APP_IDS)} shipping.yml files, found {len(manifests)}")

    apps: list[dict[str, Any]] = []
    for manifest in manifests:
        raw = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        data = require_mapping(raw, str(manifest))
        schema_version = data.get("schema_version")
        if schema_version not in (1, 2):
            fail(f"{manifest}: schema_version must be 1 or 2")

        app = require_mapping(data.get("app"), f"{manifest}: app")
        reporting = require_mapping(data.get("reporting"), f"{manifest}: reporting")
        platforms = require_strings(app.get("platforms"), f"{manifest}: app.platforms")
        if any(platform not in VALID_PLATFORMS for platform in platforms):
            fail(f"{manifest}: app.platforms contains an unsupported platform")

        if schema_version == 2:
            web = require_mapping(data.get("web"), f"{manifest}: web")
            status = require_string(app.get("status"), f"{manifest}: app.status")
            if status not in VALID_STATUSES:
                fail(f"{manifest}: app.status must be one of {sorted(VALID_STATUSES)}")
            display_name_ko = require_string(app.get("display_name_ko"), f"{manifest}: app.display_name_ko")
            tagline_ko = require_string(app.get("tagline_ko"), f"{manifest}: app.tagline_ko")
            min_os = require_string(app.get("min_os"), f"{manifest}: app.min_os")
            version = require_string(app.get("version"), f"{manifest}: app.version")
            privacy_url = optional_string(web.get("privacy"), f"{manifest}: web.privacy")
            support_url = optional_string(web.get("support"), f"{manifest}: web.support")
            store_urls = public_urls(data.get("store"), f"{manifest}: store")
            release_urls = public_urls(data.get("release"), f"{manifest}: release")
        else:
            display_name_ko = require_string(app.get("display_name"), f"{manifest}: app.display_name")
            tagline_ko = None
            min_os = None
            version = None
            status = None
            privacy_url = None
            support_url = None
            store_urls = {}
            release_urls = {}

        downloads = [
            {"platform": platform, "url": store_urls.get(platform) or release_urls.get(platform)}
            for platform in platforms
            if store_urls.get(platform) or release_urls.get(platform)
        ]
        if release_urls.get("web"):
            downloads.append({"platform": "web", "url": release_urls["web"]})
        apps.append(
            {
                "id": require_string(app.get("id"), f"{manifest}: app.id"),
                "display_name": require_string(app.get("display_name"), f"{manifest}: app.display_name"),
                "display_name_ko": display_name_ko,
                "tagline_ko": tagline_ko,
                "platforms": platforms,
                "bundle_ids": require_strings(app.get("bundle_ids"), f"{manifest}: app.bundle_ids"),
                "min_os": min_os,
                "version": version,
                "status": status,
                "downloads": downloads,
                "web": {"privacy": privacy_url, "support": support_url},
                "template": require_string(reporting.get("template"), f"{manifest}: reporting.template"),
                "locales": require_strings(reporting.get("locales"), f"{manifest}: reporting.locales"),
            }
        )

    app_ids = {app["id"] for app in apps}
    if app_ids != EXPECTED_APP_IDS:
        fail(
            f"app.id set does not match the approved {len(EXPECTED_APP_IDS)} apps: "
            f"{sorted(app_ids)}"
        )
    if len({app["template"] for app in apps}) != len(apps):
        fail("reporting.template values must be unique")
    if any(app["template"] != f"{app['id']}-bug.yml" for app in apps):
        fail("reporting.template must match <app.id>-bug.yml")

    return sorted(apps, key=lambda app: app["id"])


def json_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def form_context(app: dict[str, Any]) -> dict[str, Any]:
    platforms = set(app["platforms"])
    if platforms == {"macos"}:
        os_placeholder, device_placeholder = "macOS 15.0", "Mac"
    elif platforms == {"ios"}:
        os_placeholder, device_placeholder = "iOS 16.0", "iPhone"
    elif platforms == {"ios", "android"}:
        os_placeholder, device_placeholder = "iOS or Android", "iPhone or Android phone"
    else:
        os_placeholder, device_placeholder = "macOS or Windows", "Mac or Windows PC"

    context = {
        "app": app,
        # A build number is supplied by the app's report URL at runtime.  A
        # generated form must not advertise a stale, app-specific fallback
        # when it is opened directly instead.
        "build_placeholder": "unknown",
        "device_placeholder": device_placeholder,
        "diagnostics_description": "선택 사항입니다. 개인정보나 원본 로그를 넣지 마세요. Optional; do not include personal data or raw logs.",
        "os_placeholder": os_placeholder,
        "privacy_ack_label": "이 신고가 공개되며 민감정보를 포함하지 않았음을 확인합니다. / I understand this report is public and contains no sensitive information.",
        "public_warning_en": "This issue and its attachments are **public**. Do not include phone numbers, email addresses, real names, raw logs, user file paths, or device identifiers.",
        "public_warning_ko": "이 이슈와 첨부 파일은 **공개**됩니다. 전화번호, 이메일, 실명, 원본 로그, 사용자 파일 경로, 기기 식별자를 포함하지 마세요.",
        "screenshots_description": "개인정보를 가린 뒤 첨부해 주세요. Redact personal information before uploading.",
        "version_placeholder": app.get("version") or "1.0",
        "what_happened_placeholder": "문제를 설명해 주세요. / Describe the problem.",
    }

    if app["id"] == "gnomon":
        context.update(os_placeholder="macOS 15.6")
    elif app["id"] == "book":
        context.update(os_placeholder="iOS 17.0")
    elif app["id"] == "spamcall070":
        warning = "이 이슈와 첨부 파일은 **공개**됩니다. 차단되지 않은 실제 전화번호, 이메일, 실명, 원본 로그, 사용자 파일 경로, 기기 식별자를 포함하지 마세요."
        context.update(
            diagnostics_description="앱이 실패 블록 수와 오류 코드만 채웁니다. 실제 전화번호나 원본 로그를 추가하지 마세요.",
            os_placeholder="iOS 18.6",
            privacy_ack_label="이 신고가 공개되며 실제 전화번호나 민감정보를 포함하지 않았음을 확인합니다. / I understand this report is public and contains no real phone numbers or sensitive information.",
            public_warning_en="This issue and its attachments are **public**. Do not include real phone numbers, email addresses, real names, raw logs, user file paths, or device identifiers.",
            screenshots_description="전화번호와 개인정보를 가린 뒤 첨부해 주세요. Redact phone numbers and personal information before uploading.",
            what_happened_placeholder="실제 전화번호는 일부를 가려 주세요. / Redact any real phone numbers.",
        )
        context["public_warning_ko"] = warning
    return context


def render_forms(apps: list[dict[str, Any]]) -> dict[str, str]:
    environment = Environment(
        loader=FileSystemLoader(REPOSITORY_ROOT / "templates"),
        keep_trailing_newline=True,
        trim_blocks=False,
        undefined=StrictUndefined,
    )
    environment.filters["q"] = json_quote
    template = environment.get_template("bug.yml.j2")
    return {
        app["template"]: template.render(**form_context(app)).rstrip() + "\n"
        for app in apps
    }


def report_url(template: str) -> str:
    # Public documentation cannot infer runtime metadata; keep the URL schema
    # complete and use the required fallback value for unavailable details.
    return f"{ISSUE_URL}?{urlencode({
        'template': template,
        'version': 'unknown',
        'build': 'unknown',
        'os': 'unknown',
        'device': 'unknown',
        'diagnostics': 'unknown',
    })}"


def render_apps_json(apps: list[dict[str, Any]]) -> str:
    public_apps = [
        {
            "id": app["id"],
            "display_name": app["display_name"],
            "display_name_ko": app["display_name_ko"],
            "tagline_ko": app["tagline_ko"],
            "platforms": app["platforms"],
            "min_os": app["min_os"],
            "version": app["version"],
            "status": app["status"],
            "downloads": app["downloads"],
            "web": app["web"],
            "report_template": app["template"],
            "report_url": report_url(app["template"]),
        }
        for app in apps
    ]
    public_payload = {"schema_version": 2, "apps": public_apps}
    return json.dumps(public_payload, ensure_ascii=False, indent=2) + "\n"


def render_labels(apps: list[dict[str, Any]]) -> str:
    labels = [f"app:{app['id']}" for app in apps]
    labels.extend(COMMON_LABELS)
    return "\n".join(sorted(labels)) + "\n"


def swift_property_name(app_id: str) -> str:
    parts = [part for part in re.split(r"[^A-Za-z0-9]+", app_id) if part]
    if not parts:
        fail(f"cannot derive a Swift property name from app.id {app_id!r}")

    name = parts[0].lower() + "".join(part[:1].upper() + part[1:] for part in parts[1:])
    if name[0].isdigit() or name in SWIFT_KEYWORDS:
        name = "app" + name[:1].upper() + name[1:]
    return name


def render_swift_targets(apps: list[dict[str, Any]]) -> str:
    properties = [swift_property_name(app["id"]) for app in apps]
    if len(set(properties)) != len(properties):
        fail("generated Swift property names would collide")

    lines = [
        "// This file is generated from shipping.yml manifests.",
        "// Run: uv run python scripts/generate.py",
        "// Do not edit by hand.",
        "",
        "public enum ReportTargets {",
    ]
    for app, property_name in zip(apps, properties):
        lines.extend(
            [
                f"    public static let {property_name} = ReportTarget(",
                f"        appID: {json.dumps(app['id'], ensure_ascii=False)},",
                f"        displayName: {json.dumps(app['display_name'], ensure_ascii=False)},",
                f"        template: {json.dumps(app['template'], ensure_ascii=False)}",
                "    )",
                "",
            ]
        )

    lines.append("    public static let all: [ReportTarget] = [")
    lines.extend(f"        {property_name}," for property_name in properties)
    lines.extend(["    ]", ""])
    lines.extend([
        "    public static func target(forAppID appID: String) -> ReportTarget? {",
        "        switch appID {",
    ])
    for app, property_name in zip(apps, properties):
        lines.append(f"        case {json.dumps(app['id'], ensure_ascii=False)}: return {property_name}")
    lines.extend([
        "        default: return nil",
        "        }",
        "    }",
        "}",
        "",
    ])
    return "\n".join(lines)


def render_readme(apps: list[dict[str, Any]]) -> str:
    links = "\n".join(
        f"- [{app['display_name']} 버그 신고 / Bug report]({report_url(app['template'])})"
        for app in apps
    )
    return (
        "## 신고하기 / Report a bug\n\n"
        "<!-- BEGIN GENERATED REPORT LINKS -->\n"
        f"{links}\n"
        "<!-- END GENERATED REPORT LINKS -->\n\n"
        "앱 안의 **GitHub에 신고 / Report on GitHub** 버튼을 사용하면 앱 버전과 운영체제 정보가 자동으로 채워집니다.\n"
        "Using the in-app report button pre-fills the app version and operating-system details.\n"
    )


def write(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def validate_public_outputs(outputs: dict[Path, str]) -> None:
    for path, contents in outputs.items():
        lowered = contents.lower()
        for marker in PRIVATE_MARKERS:
            if marker.lower() in lowered:
                fail(f"{path.relative_to(REPOSITORY_ROOT)} would expose private identifier {marker}")
        if "mailto:" in lowered:
            fail(f"{path.relative_to(REPOSITORY_ROOT)} would expose an email reporting path")


def main() -> None:
    args = parse_args()
    shipping_root = args.shipping_root.expanduser().resolve()
    swift_output = args.swift_output.expanduser().resolve()
    apps = load_apps(shipping_root)
    forms = render_forms(apps)

    readme_path = REPOSITORY_ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    updated_readme, replacements = README_SECTION.subn(render_readme(apps), readme)
    if replacements != 1:
        fail("README.md must contain exactly one report section before public visibility")

    outputs = {
        **{
            REPOSITORY_ROOT / ".github" / "ISSUE_TEMPLATE" / filename: contents
            for filename, contents in forms.items()
        },
        REPOSITORY_ROOT / "apps.json": render_apps_json(apps),
        REPOSITORY_ROOT / "labels.txt": render_labels(apps),
        readme_path: updated_readme,
        swift_output: render_swift_targets(apps),
    }
    validate_public_outputs(outputs)

    if args.check:
        stale = [
            str(path.relative_to(REPOSITORY_ROOT))
            for path, contents in outputs.items()
            if not path.exists() or path.read_text(encoding="utf-8") != contents
        ]
        if stale:
            fail(f"generated artifacts are out of date: {', '.join(stale)}")
        print(f"verified {len(forms)} issue forms and ReportKit targets from {shipping_root}")
        return

    for path, contents in outputs.items():
        write(path, contents)
    print(f"generated {len(forms)} issue forms and ReportKit targets from {shipping_root}")


if __name__ == "__main__":
    main()
