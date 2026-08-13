#!/usr/bin/env python3
"""Validate source metadata and generated site structure without extra packages."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
KEY_VALUE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
RELEASE_START_RE = re.compile(r"^- version:\s*(.*)$")
RELEASE_KEY_RE = re.compile(r"^  ([A-Za-z0-9_-]+):\s*(.*)$")


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.links: list[str] = []
        self.site_nav_links: list[tuple[str, str, set[str]]] = []
        self.quick_links: list[str] = []
        self.site_brand_href = ""
        self.breadcrumb_home_href = ""
        self.site_nav_label = ""
        self.html_lang = ""
        self.site_header_count = 0
        self.site_footer_count = 0
        self.breadcrumb_count = 0
        self.quick_links_count = 0
        self.language_switcher_count = 0
        self.translation_notice_count = 0
        self.h1_count = 0
        self.release_finder_count = 0
        self.release_query_count = 0
        self.release_version_count = 0
        self.release_entry_count = 0
        self.release_change_count = 0
        self.release_highlight_title_count = 0
        self.title_text: list[str] = []
        self.description = ""
        self._in_title = False
        self._in_site_nav = False
        self._in_breadcrumb = False
        self._in_quick_links = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        element_id = attributes.get("id")

        if tag == "html":
            self.html_lang = (attributes.get("lang") or "").strip()
        if element_id:
            self.ids.append(element_id)
        if "language-switcher" in classes:
            self.language_switcher_count += 1
        if "site-footer__translation-notice" in classes:
            self.translation_notice_count += 1
        if "data-release-finder" in attributes:
            self.release_finder_count += 1
        if "data-release-query" in attributes:
            self.release_query_count += 1
        if "data-release-version-filter" in attributes:
            self.release_version_count += 1
        if "data-release-entry" in attributes:
            self.release_entry_count += 1
        if "data-release-change" in attributes:
            self.release_change_count += 1
        if "release-highlight__title" in classes:
            self.release_highlight_title_count += 1

        if tag == "header" and "site-header" in classes:
            self.site_header_count += 1
        elif tag == "footer" and "site-footer" in classes:
            self.site_footer_count += 1
        elif tag == "nav" and "breadcrumb" in classes:
            self.breadcrumb_count += 1
            self._in_breadcrumb = True
        elif tag == "nav" and "site-nav" in classes:
            self._in_site_nav = True
            self.site_nav_label = (attributes.get("aria-label") or "").strip()
        elif tag == "section" and "quick-links" in classes:
            self.quick_links_count += 1
            self._in_quick_links = True

        if tag == "a":
            href = attributes.get("href") or ""
            if attributes.get("name"):
                self.ids.append(attributes["name"] or "")
            if href:
                self.links.append(href)
                if "site-brand" in classes:
                    self.site_brand_href = href
                if self._in_breadcrumb and not self.breadcrumb_home_href:
                    self.breadcrumb_home_href = href
                if self._in_quick_links:
                    self.quick_links.append(href)
                if self._in_site_nav:
                    rel = set((attributes.get("rel") or "").split())
                    self.site_nav_links.append((href, attributes.get("target") or "", rel))
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and attributes.get("name", "").lower() == "description":
            self.description = (attributes.get("content") or "").strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "nav" and self._in_breadcrumb:
            self._in_breadcrumb = False
        elif tag == "nav" and self._in_site_nav:
            self._in_site_nav = False
        elif tag == "section" and self._in_quick_links:
            self._in_quick_links = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_text.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_text).split())


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}

    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        parsed = KEY_VALUE_RE.match(line)
        if parsed:
            values[parsed.group(1)] = parsed.group(2).strip().strip("\"'")
    return values


def parse_document(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8-sig"))
    return parser


def parse_release_records(path: Path) -> list[dict[str, str]]:
    releases: list[dict[str, str]] = []
    current: dict[str, str] | None = None

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        start = RELEASE_START_RE.match(line)
        if start:
            if current:
                releases.append(current)
            current = {"version": start.group(1).strip().strip("\"'")}
            continue

        if current:
            parsed = RELEASE_KEY_RE.match(line)
            if parsed:
                current[parsed.group(1)] = parsed.group(2).strip().strip("\"'")

    if current:
        releases.append(current)
    return releases


def release_data_checks(root: Path, releases_path: Path) -> list[str]:
    errors: list[str] = []
    if not releases_path.exists():
        return [f"Missing release data: {releases_path}"]

    releases = parse_release_records(releases_path)
    if not releases:
        return [f"{releases_path}: no release records found"]

    required = ("version", "slug", "date", "pdf", "summary", "source_pages", "highlights", "categories")
    versions: set[str] = set()
    slugs: set[str] = set()
    current_releases = 0

    for index, release in enumerate(releases, start=1):
        label = release.get("version") or f"#{index}"
        for field in required:
            if field not in release:
                errors.append(f"{releases_path}: release {label} missing '{field}'")

        version = release.get("version", "")
        slug = release.get("slug", "")
        if version in versions:
            errors.append(f"{releases_path}: duplicate release version '{version}'")
        if slug in slugs:
            errors.append(f"{releases_path}: duplicate release slug '{slug}'")
        versions.add(version)
        slugs.add(slug)

        if release.get("current", "").lower() == "true":
            current_releases += 1

        date_iso = release.get("date_iso", "")
        if date_iso and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_iso):
            errors.append(f"{releases_path}: release {label} has invalid date_iso '{date_iso}'")

        pdf = release.get("pdf", "")
        if pdf.startswith("/"):
            target = root / unquote(pdf.lstrip("/"))
            if not target.exists():
                errors.append(f"{releases_path}: release {label} points to missing PDF {pdf}")
        elif pdf:
            errors.append(f"{releases_path}: release {label} PDF must use a root-relative path")

    if current_releases != 1:
        errors.append(f"{releases_path}: expected exactly one current release, found {current_releases}")

    try:
        version_order = [tuple(int(part) for part in release["version"].split(".")) for release in releases]
        if version_order != sorted(version_order, reverse=True):
            errors.append(f"{releases_path}: releases must be ordered newest first")
    except (KeyError, ValueError):
        errors.append(f"{releases_path}: release versions must be dot-separated numbers")

    return errors


def release_checks(root: Path) -> list[str]:
    errors: list[str] = []
    for releases_path in (
        root / "_data" / "releases.yml",
        root / "_data" / "ubiquity_releases.yml",
    ):
        errors.extend(release_data_checks(root, releases_path))

    for page_path in (
        root / "chapters" / "FTOptix_overview.html",
        root / "chapters" / "Ubiquity_releases.html",
    ):
        if not page_path.exists():
            errors.append(f"Missing release page: {page_path}")
        elif "{% include release-page.html %}" not in page_path.read_text(encoding="utf-8-sig"):
            errors.append(f"{page_path}: missing shared release-page include")

    template_path = root / "_includes" / "release-history.html"
    if not template_path.exists():
        errors.append(f"Missing release timeline template: {template_path}")
    else:
        template_text = template_path.read_text(encoding="utf-8-sig")
        for marker in (
            'class="release-timeline"',
            "data-release-finder",
            "data-release-query",
            "data-release-version-filter",
            "highlight.title",
            "highlight.description",
        ):
            if marker not in template_text:
                errors.append(f"{template_path}: missing release timeline marker {marker}")
        for obsolete in ("localized_", "include.translations", "release_translations"):
            if obsolete in template_text:
                errors.append(f"{template_path}: obsolete translation logic '{obsolete}' remains")

    script_path = root / "assets" / "js" / "site.js"
    if not script_path.exists():
        errors.append(f"Missing site script: {script_path}")
    else:
        script_text = script_path.read_text(encoding="utf-8-sig")
        for marker in ("initReleaseFinders", "data-release-query-param", "data-release-version-param"):
            if marker not in script_text:
                errors.append(f"{script_path}: missing release finder marker {marker}")
        if "data-language-link" in script_text:
            errors.append(f"{script_path}: obsolete language-link behavior remains")

    return errors


def source_checks(root: Path) -> list[str]:
    errors: list[str] = []
    localization_paths = (
        root / "it",
        root / "pl",
        root / "zh",
        root / "fur",
        root / "chapters" / "it",
        root / "chapters" / "pl",
        root / "chapters" / "zh",
        root / "chapters" / "fur",
        root / "_data" / "languages.yml",
        root / "_data" / "translated_pages.yml",
        root / "_data" / "locales",
        root / "_data" / "release_translations",
        root / "_data" / "nis2_checklist",
        root / "_includes" / "language-switcher.html",
        root / "_includes" / "nis2-checklist",
        root / "_layouts" / "nis2-checklist.html",
    )
    for path in localization_paths:
        if path.exists():
            errors.append(f"Obsolete localization artifact remains: {path}")

    source_files = [
        root / "index.html",
        *sorted((root / "chapters").rglob("*.html")),
    ]
    for page in source_files:
        front_matter = parse_front_matter(page)
        for required in ("layout", "title", "description"):
            if not front_matter.get(required):
                errors.append(f"{page}: missing front-matter field '{required}'")
        for obsolete in ("lang", "translation_key"):
            if obsolete in front_matter:
                errors.append(f"{page}: obsolete front-matter field '{obsolete}'")

    localization_markers = (
        "site.data.locales",
        "site.data.languages",
        "site.data.translated_pages",
        "site.data.release_translations",
        "site.data.nis2_checklist",
        "page.lang",
        "translation_key:",
        "data-language-link",
        "language-switcher",
        "site-footer__translation-notice",
        "hreflang=",
    )
    render_files = [
        root / "index.html",
        *sorted((root / "chapters").rglob("*.html")),
        *sorted((root / "_includes").rglob("*.html")),
        *sorted((root / "_layouts").rglob("*.html")),
        *sorted((root / "assets").rglob("*.js")),
        *sorted((root / "assets").rglob("*.css")),
    ]
    for path in render_files:
        text = path.read_text(encoding="utf-8-sig")
        for marker in localization_markers:
            if marker in text:
                errors.append(f"{path}: obsolete localization marker '{marker}'")

    index_text = (root / "index.html").read_text(encoding="utf-8-sig")
    if "{% include site-header.html %}" in index_text:
        errors.append(f"{root / 'index.html'}: homepage must not render the top bar")
    if 'class="quick-links"' not in index_text or "Day-to-Day Essentials" not in index_text:
        errors.append(f"{root / 'index.html'}: missing Day-to-Day Essentials section")
    if "assets/js/site.js" not in index_text:
        errors.append(f"{root / 'index.html'}: homepage must load shared link behavior")

    header_path = root / "_includes" / "site-header.html"
    if header_path.exists():
        header_text = header_path.read_text(encoding="utf-8-sig")
        if header_text.count('target="_blank"') != 5:
            errors.append(f"{header_path}: all five top-bar resource links must open a new tab")
        if header_text.count('rel="noopener noreferrer"') != 5:
            errors.append(f"{header_path}: all five top-bar resource links need safe rel attributes")

    site_script_path = root / "assets" / "js" / "site.js"
    if site_script_path.exists():
        site_script = site_script_path.read_text(encoding="utf-8-sig")
        for marker in (
            'querySelectorAll("a[href]")',
            'link.setAttribute("target", "_blank")',
            'rel.add("noopener")',
            'rel.add("noreferrer")',
        ):
            if marker not in site_script:
                errors.append(f"{site_script_path}: missing external-link behavior '{marker}'")

    materials_root = root / "pdf"
    expected_material_folders = {"cybersecurity", "ftoptix", "optixedge", "ubiquity"}
    if not materials_root.exists():
        errors.append(f"Missing materials directory: {materials_root}")
    else:
        root_materials = sorted(path.name for path in materials_root.iterdir() if path.is_file())
        if root_materials:
            errors.append(f"{materials_root}: materials must be classified into subfolders: {', '.join(root_materials)}")
        actual_material_folders = {path.name for path in materials_root.iterdir() if path.is_dir()}
        missing_material_folders = sorted(expected_material_folders - actual_material_folders)
        if missing_material_folders:
            errors.append(f"{materials_root}: missing material folders: {', '.join(missing_material_folders)}")

        nis2_name = "New_European_CyberSecurityRegulations_NI2_Checklist_v2.0.html"
        nis2_materials = sorted((materials_root / "cybersecurity").rglob(nis2_name))
        expected_nis2_material = materials_root / "cybersecurity" / nis2_name
        if nis2_materials != [expected_nis2_material]:
            errors.append(f"{materials_root / 'cybersecurity'}: keep exactly one canonical NIS2 HTML material")

    resources_path = root / "_data" / "resources.yml"
    if not resources_path.exists():
        errors.append(f"Missing resource catalog: {resources_path}")
        return errors

    current: dict[str, str] = {}
    resources: list[dict[str, str]] = []
    for raw_line in resources_path.read_text(encoding="utf-8-sig").splitlines():
        if raw_line.startswith("- "):
            if current:
                resources.append(current)
            current = {}
            raw_line = raw_line[2:]
        else:
            raw_line = raw_line.strip()
        parsed = KEY_VALUE_RE.match(raw_line)
        if parsed:
            current[parsed.group(1)] = parsed.group(2).strip().strip("\"'")
    if current:
        resources.append(current)

    titles: set[str] = set()
    for index, resource in enumerate(resources, start=1):
        title = resource.get("title", "")
        if not title:
            errors.append(f"{resources_path}: resource #{index} has no title")
        elif title in titles:
            errors.append(f"{resources_path}: duplicate resource title '{title}'")
        titles.add(title)

        for required in ("summary", "url", "topic", "journey", "level", "format", "language", "source"):
            if not resource.get(required):
                errors.append(f"{resources_path}: '{title or index}' missing '{required}'")

        url = resource.get("url", "")
        if url.startswith("/"):
            target = root / unquote(url.lstrip("/"))
            if not target.exists():
                errors.append(f"{resources_path}: '{title}' points to missing local file {url}")

    errors.extend(release_checks(root))
    return errors


def resolve_target(root: Path, page: Path, href: str, base_path: str) -> tuple[Path | None, str]:
    if not href or href.startswith(("#", "{{", "mailto:", "tel:", "javascript:")):
        return None, ""

    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None, parsed.fragment

    raw_path = unquote(parsed.path)
    if base_path and raw_path.startswith(base_path + "/"):
        raw_path = raw_path[len(base_path) + 1 :]
        target = root / raw_path
    elif raw_path.startswith("/"):
        target = root / raw_path.lstrip("/")
    elif raw_path:
        target = page.parent / raw_path
    else:
        target = page

    if raw_path.endswith("/"):
        target = target / "index.html"
    return target.resolve(), unquote(parsed.fragment)


def built_checks(root: Path, base_path: str) -> list[str]:
    errors: list[str] = []
    pages = sorted(root.rglob("*.html"))
    parsed_pages = {page.resolve(): parse_document(page) for page in pages}
    expected_nav_links = [
        f"{base_path}/chapters/Learning_material_Videos.html",
        "https://eng2e.seismic.com/ls/5d78bc76-77f9-460a-a446-4685520db077/HRZbG6dVdtwIQipW#/content/9229e75b-dc4e-4165-bcc6-90450dc0fe4b",
        "https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet",
        "https://engage.rockwellautomation.com/communities/forums/forums-home?CommunityKey=0cbb1b6c-055d-48db-8d38-d24850beeec9",
        "https://rockwellautomation.custhelp.com/app/home",
    ]
    expected_quick_links = [
        "chapters/Learning_material_Videos.html",
        "https://eng2e.seismic.com/ls/5d78bc76-77f9-460a-a446-4685520db077/HRZbG6dVdtwIQipW#/content/9229e75b-dc4e-4165-bcc6-90450dc0fe4b",
        "https://github.com/FactoryTalk-Optix/NetLogic_CheatSheet",
        "https://engage.rockwellautomation.com/communities/forums/forums-home?CommunityKey=0cbb1b6c-055d-48db-8d38-d24850beeec9",
        "https://rockwellautomation.custhelp.com/app/home",
    ]
    expected_home = f"{base_path}/"

    for page in pages:
        relative = page.relative_to(root)
        document = parsed_pages[page.resolve()]
        duplicate_ids = sorted({item for item in document.ids if document.ids.count(item) > 1})
        if duplicate_ids:
            errors.append(f"{relative}: duplicate IDs: {', '.join(duplicate_ids)}")

        is_site_page = "pdf" not in relative.parts
        if is_site_page:
            is_home = relative == Path("index.html")
            if document.html_lang != "en":
                errors.append(f"{relative}: expected html lang 'en', found '{document.html_lang}'")
            if not document.title:
                errors.append(f"{relative}: missing document title")
            if not document.description:
                errors.append(f"{relative}: missing meta description")
            if document.h1_count != 1:
                errors.append(f"{relative}: expected one h1, found {document.h1_count}")
            if document.site_footer_count != 1:
                errors.append(f"{relative}: expected one shared footer, found {document.site_footer_count}")
            if document.language_switcher_count:
                errors.append(f"{relative}: language switcher must not be rendered")
            if document.translation_notice_count:
                errors.append(f"{relative}: translation notice must not be rendered")

            if is_home:
                if document.site_header_count != 0:
                    errors.append(f"{relative}: homepage must not render the top bar")
                if document.breadcrumb_count != 0:
                    errors.append(f"{relative}: homepage must not render a breadcrumb")
                if document.quick_links_count != 1:
                    errors.append(f"{relative}: expected one Day-to-Day Essentials section")
                if document.quick_links != expected_quick_links:
                    errors.append(f"{relative}: Day-to-Day Essentials links are incomplete or out of order")
            else:
                if document.site_header_count != 1:
                    errors.append(f"{relative}: expected one shared site header, found {document.site_header_count}")
                if document.breadcrumb_count != 1:
                    errors.append(f"{relative}: expected one breadcrumb, found {document.breadcrumb_count}")
                if document.quick_links_count:
                    errors.append(f"{relative}: Day-to-Day Essentials section belongs only on the homepage")
                if document.site_nav_label != "Day-to-Day Essentials":
                    errors.append(f"{relative}: top bar has unexpected label '{document.site_nav_label}'")

                nav_hrefs = [href for href, _, _ in document.site_nav_links]
                if nav_hrefs != expected_nav_links:
                    errors.append(f"{relative}: top-bar links do not match Day-to-Day Essentials")
                for href, target, rel in document.site_nav_links:
                    if target != "_blank":
                        errors.append(f"{relative}: top-bar link '{href}' must open in a new tab")
                    if not {"noopener", "noreferrer"}.issubset(rel):
                        errors.append(f"{relative}: top-bar link '{href}' is missing safe rel attributes")

                if document.site_brand_href != expected_home:
                    errors.append(f"{relative}: brand must link to {expected_home}")
                if document.breadcrumb_home_href != expected_home:
                    errors.append(f"{relative}: breadcrumb must link to {expected_home}")

            if relative.name == "FTOptix_overview.html":
                expected_release_counts = {
                    "feature finder": (document.release_finder_count, 1),
                    "keyword input": (document.release_query_count, 1),
                    "version selector": (document.release_version_count, 1),
                    "release entries": (document.release_entry_count, 5),
                    "documented changes": (document.release_change_count, 158),
                    "named key changes": (document.release_highlight_title_count, 20),
                }
                for label, (actual, expected) in expected_release_counts.items():
                    if actual != expected:
                        errors.append(f"{relative}: expected {expected} {label}, found {actual}")

            if relative.name == "Ubiquity_releases.html":
                expected_release_counts = {
                    "feature finder": (document.release_finder_count, 1),
                    "keyword input": (document.release_query_count, 1),
                    "version selector": (document.release_version_count, 1),
                    "release entries": (document.release_entry_count, 4),
                    "documented changes": (document.release_change_count, 66),
                    "named key changes": (document.release_highlight_title_count, 20),
                }
                for label, (actual, expected) in expected_release_counts.items():
                    if actual != expected:
                        errors.append(f"{relative}: expected {expected} {label}, found {actual}")

        for href in document.links:
            target, fragment = resolve_target(root, page, href, base_path)
            if target is None:
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{relative}: broken local link '{href}'")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_document = parsed_pages.get(target.resolve())
                if target_document and fragment not in target_document.ids:
                    errors.append(f"{relative}: missing fragment target '{href}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--mode", choices=("source", "releases", "built"), required=True)
    parser.add_argument("--base-path", default="/LearningFTOptix")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.exists():
        print(f"Root does not exist: {root}", file=sys.stderr)
        return 2

    if args.mode == "source":
        errors = source_checks(root)
    elif args.mode == "releases":
        errors = release_checks(root)
    else:
        errors = built_checks(root, args.base_path.rstrip("/"))

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    print(f"Site {args.mode} checks passed for {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
