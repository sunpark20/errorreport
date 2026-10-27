import json
import unittest
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

import yaml

try:
    from scripts import generate
except ModuleNotFoundError:  # direct `python scripts/test_generate.py`
    import generate


class GeneratorTests(unittest.TestCase):
    def test_default_manifests_produce_the_approved_catalog(self):
        apps = generate.load_apps(generate.DEFAULT_SHIPPING_ROOT)
        self.assertEqual(len(apps), 15)
        self.assertEqual({app["id"] for app in apps}, generate.EXPECTED_APP_IDS)

    def test_report_urls_use_only_issue_form_fields(self):
        url = generate.report_url("gnomon-bug.yml")
        query = dict(parse_qsl(urlsplit(url).query))
        self.assertEqual(
            set(query), {"template", "version", "build", "os", "device", "diagnostics"}
        )
        self.assertNotIn("labels", query)
        self.assertNotIn("body", query)

    def test_swift_catalog_uses_manifest_ids_and_safe_names(self):
        apps = generate.load_apps(generate.DEFAULT_SHIPPING_ROOT)
        swift = generate.render_swift_targets(apps)
        self.assertIn('appID: "breaklock-timer"', swift)
        self.assertIn("public static let breaklockTimer", swift)
        self.assertIn('template: "yt-bulk-downloader-bug.yml"', swift)

    def test_apps_json_has_no_private_markers(self):
        apps = generate.load_apps(generate.DEFAULT_SHIPPING_ROOT)
        payload = json.loads(generate.render_apps_json(apps))
        text = json.dumps(payload, ensure_ascii=False).lower()
        for marker in generate.PRIVATE_MARKERS:
            self.assertNotIn(marker.lower(), text)

    def test_generated_forms_match_report_url_field_ids(self):
        expected_fields = {"version", "build", "os", "device", "diagnostics"}
        for app in generate.load_apps(generate.DEFAULT_SHIPPING_ROOT):
            form_path = Path(generate.REPOSITORY_ROOT) / ".github" / "ISSUE_TEMPLATE" / app["template"]
            form = yaml.safe_load(form_path.read_text(encoding="utf-8"))
            field_ids = {
                item["id"]
                for item in form["body"]
                if item.get("type") in {"input", "textarea"} and "id" in item
            }
            self.assertTrue(expected_fields <= field_ids, app["id"])


if __name__ == "__main__":
    unittest.main()
