from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent

SRC_DIR = PROJECT_ROOT / "src"
TEMPLATES_DIR = SRC_DIR / "templates"
COMPONENTS_DIR = SRC_DIR / "components"
DATA_DIR = SRC_DIR / "data"
ASSETS_DIR = SRC_DIR / "assets"

DIST_DIR = PROJECT_ROOT / "dist"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

PAGES = [
    {
        "name": "Home",
        "slug": "",
        "template": "index.html",
    },
    {
        "name": "About",
        "slug": "about",
        "template": "about.html",
    },
    {
        "name": "Ministries",
        "slug": "ministries",
        "template": "ministries.html",
    },
    {
        "name": "Sermons",
        "slug": "sermons",
        "template": "sermons.html",
    },
    {
        "name": "Programmes",
        "slug": "programmes",
        "template": "programmes.html",
    },
    {
        "name": "Events",
        "slug": "events",
        "template": "events.html",
    },
    {
        "name": "Give",
        "slug": "give",
        "template": "give.html",
    },
    {
        "name": "Contact",
        "slug": "contact",
        "template": "contact.html",
    },
]


# ============================================================
# VALIDATION
# ============================================================

class BuildValidationError(Exception):
    """Raised when source content is unsafe or invalid to build."""


warnings: list[str] = []


def warn(message: str) -> None:
    warnings.append(message)


def fail(message: str) -> None:
    raise BuildValidationError(message)


# ============================================================
# JSON LOADING
# ============================================================

def load_json(filename: str) -> dict[str, Any]:
    path = DATA_DIR / filename

    if not path.exists():
        fail(f"Required data file does not exist: {path}")

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        fail(
            f"Invalid JSON in {filename}: "
            f"line {exc.lineno}, column {exc.colno}: {exc.msg}"
        )

    if not isinstance(data, dict):
        fail(f"{filename} must contain a JSON object at the top level.")

    return data


def load_all_data() -> dict[str, dict[str, Any]]:
    return {
        "site": load_json("site.json"),
        "ministries": load_json("ministries.json"),
        "programmes": load_json("programmes.json"),
        "sermons": load_json("sermons.json"),
        "events": load_json("events.json"),
        "testimonials": load_json("testimonials.json"),
    }


# ============================================================
# GENERIC HELPERS
# ============================================================

def require_list(
    data: dict[str, Any],
    key: str,
    filename: str,
) -> list[Any]:

    if key not in data:
        fail(f"{filename} must contain top-level key '{key}'.")

    value = data[key]

    if not isinstance(value, list):
        fail(f"{filename}.{key} must be a list.")

    return value


def published_only(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    A missing published field defaults to False.

    This prevents accidentally publishing content merely because
    the author forgot to add the publication flag.
    """

    return [
        record
        for record in records
        if isinstance(record, dict)
        and record.get("published") is True
    ]


def check_duplicate_ids(
    records: list[dict[str, Any]],
    collection_name: str,
) -> None:

    seen: set[str] = set()

    for record in records:
        record_id = record.get("id")

        if record_id is None:
            continue

        if not isinstance(record_id, str) or not record_id.strip():
            fail(
                f"{collection_name} contains a record "
                f"with an invalid id."
            )

        if record_id in seen:
            fail(
                f"Duplicate id '{record_id}' found in "
                f"{collection_name}."
            )

        seen.add(record_id)


def require_string(
    record: dict[str, Any],
    field: str,
    description: str,
) -> str:

    value = record.get(field)

    if not isinstance(value, str) or not value.strip():
        fail(
            f"{description} requires a non-empty "
            f"'{field}' value."
        )

    return value


# ============================================================
# SITE.JSON VALIDATION
# ============================================================

def validate_site_data(site_data: dict[str, Any]) -> None:

    site = site_data.get("site")

    if not isinstance(site, dict):
        fail("site.json must contain a 'site' object.")

    if not site.get("name"):
        warn("site.name has not yet been supplied.")

    if not site.get("vision"):
        warn("site.vision has not yet been supplied.")

    if not site.get("mission"):
        warn("site.mission has not yet been supplied.")

    if not site.get("history"):
        warn("site.history has not yet been supplied.")

    values = site.get("values", [])

    if not values:
        warn("site.values is currently empty.")

    # --------------------------------------------------------
    # Leadership
    # --------------------------------------------------------

    leadership = site_data.get("leadership", [])

    if not isinstance(leadership, list):
        fail("site.json leadership must be a list.")

    leadership_dicts = [
        item for item in leadership
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        leadership_dicts,
        "site.json leadership",
    )

    for pastor in published_only(leadership_dicts):

        require_string(
            pastor,
            "name",
            "Published leadership record",
        )

        require_string(
            pastor,
            "mobile",
            f"Published leadership record "
            f"'{pastor.get('id', 'unknown')}'",
        )

        whatsapp = pastor.get("whatsapp")

        if whatsapp not in (True, False, None):
            fail(
                f"Leadership record "
                f"'{pastor.get('id')}' has invalid "
                f"whatsapp value. Use true, false or null."
            )

    # --------------------------------------------------------
    # Contact
    # --------------------------------------------------------

    contact = site_data.get("contact", {})

    if not isinstance(contact, dict):
        fail("site.json contact must be an object.")

    if not contact.get("phone"):
        warn("No official main church telephone supplied.")

    if not contact.get("whatsapp"):
        warn("No official church WhatsApp number supplied.")

    if not contact.get("email"):
        warn("No official church email supplied.")

    if not contact.get("address"):
        warn("No textual church address supplied.")

    # --------------------------------------------------------
    # Service times
    # --------------------------------------------------------

    service_times = site_data.get("service_times", [])

    if not isinstance(service_times, list):
        fail("site.json service_times must be a list.")

    service_dicts = [
        item for item in service_times
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        service_dicts,
        "site.json service_times",
    )

    for service in published_only(service_dicts):

        require_string(
            service,
            "name",
            "Published service time",
        )

        require_string(
            service,
            "day",
            f"Service '{service.get('id', 'unknown')}'",
        )

        if not (
            service.get("display_time")
            or (
                service.get("start_time")
                and service.get("end_time")
            )
        ):
            fail(
                f"Published service "
                f"'{service.get('id', 'unknown')}' "
                f"requires display_time or start/end times."
            )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location = site_data.get("location", {})

    if not isinstance(location, dict):
        fail("site.json location must be an object.")

    if not location.get("google_maps_url"):
        warn("Google Maps URL has not yet been supplied.")

    # --------------------------------------------------------
    # Social links
    # --------------------------------------------------------

    social_links = site_data.get("social_links", [])

    if not isinstance(social_links, list):
        fail("site.json social_links must be a list.")

    for link in published_only(
        [
            item
            for item in social_links
            if isinstance(item, dict)
        ]
    ):
        require_string(
            link,
            "platform",
            "Published social link",
        )

        require_string(
            link,
            "url",
            f"Social link '{link.get('platform', 'unknown')}'",
        )

    # --------------------------------------------------------
    # Giving
    # --------------------------------------------------------

    giving = site_data.get("giving", {})

    if not isinstance(giving, dict):
        fail("site.json giving must be an object.")

    if not giving.get("methods"):
        warn("No giving methods have yet been supplied.")


# ============================================================
# COLLECTION VALIDATION
# ============================================================

def validate_ministries(data: dict[str, Any]) -> None:

    ministries = require_list(
        data,
        "ministries",
        "ministries.json",
    )

    records = [
        item for item in ministries
        if isinstance(item, dict)
    ]

    check_duplicate_ids(records, "ministries.json")

    if not records:
        warn("ministries.json currently contains no ministries.")

    for ministry in published_only(records):

        require_string(
            ministry,
            "id",
            "Published ministry",
        )

        require_string(
            ministry,
            "name",
            "Published ministry",
        )


def validate_programmes(data: dict[str, Any]) -> None:

    programmes = require_list(
        data,
        "programmes",
        "programmes.json",
    )

    records = [
        item for item in programmes
        if isinstance(item, dict)
    ]

    check_duplicate_ids(records, "programmes.json")

    if not records:
        warn("programmes.json currently contains no programmes.")

    for programme in published_only(records):

        programme_id = require_string(
            programme,
            "id",
            "Published programme",
        )

        require_string(
            programme,
            "name",
            f"Programme '{programme_id}'",
        )

        require_string(
            programme,
            "day",
            f"Programme '{programme_id}'",
        )

        if not (
            programme.get("display_time")
            or (
                programme.get("start_time")
                and programme.get("end_time")
            )
        ):
            fail(
                f"Published programme '{programme_id}' "
                f"requires display_time or start/end times."
            )


def validate_sermons(data: dict[str, Any]) -> None:

    sermons = require_list(
        data,
        "sermons",
        "sermons.json",
    )

    records = [
        item for item in sermons
        if isinstance(item, dict)
    ]

    check_duplicate_ids(records, "sermons.json")

    if not records:
        warn("sermons.json currently contains no sermons.")

    for sermon in published_only(records):

        sermon_id = require_string(
            sermon,
            "id",
            "Published sermon",
        )

        require_string(
            sermon,
            "title",
            f"Sermon '{sermon_id}'",
        )

        if not (
            sermon.get("youtube_id")
            or sermon.get("youtube_url")
        ):
            fail(
                f"Published sermon '{sermon_id}' requires "
                f"youtube_id or youtube_url."
            )


def validate_events(data: dict[str, Any]) -> None:

    events = require_list(
        data,
        "events",
        "events.json",
    )

    records = [
        item for item in events
        if isinstance(item, dict)
    ]

    check_duplicate_ids(records, "events.json")

    if not records:
        warn("events.json currently contains no events.")

    for event in published_only(records):

        event_id = require_string(
            event,
            "id",
            "Published event",
        )

        require_string(
            event,
            "name",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "date",
            f"Event '{event_id}'",
        )


def validate_testimonials(data: dict[str, Any]) -> None:

    testimonials = require_list(
        data,
        "testimonials",
        "testimonials.json",
    )

    records = [
        item for item in testimonials
        if isinstance(item, dict)
    ]

    check_duplicate_ids(records, "testimonials.json")

    for testimonial in published_only(records):

        testimonial_id = require_string(
            testimonial,
            "id",
            "Published testimonial",
        )

        if testimonial.get("permission_confirmed") is not True:
            fail(
                f"Published testimonial '{testimonial_id}' "
                f"does not have publication permission."
            )

        require_string(
            testimonial,
            "text",
            f"Testimonial '{testimonial_id}'",
        )


def validate_all_data(
    data: dict[str, dict[str, Any]],
) -> None:

    validate_site_data(data["site"])
    validate_ministries(data["ministries"])
    validate_programmes(data["programmes"])
    validate_sermons(data["sermons"])
    validate_events(data["events"])
    validate_testimonials(data["testimonials"])


# ============================================================
# PREPARE TEMPLATE DATA
# ============================================================

def prepare_context(
    data: dict[str, dict[str, Any]],
) -> dict[str, Any]:

    site_data = data["site"]

    leadership = published_only(
        [
            item
            for item in site_data.get("leadership", [])
            if isinstance(item, dict)
        ]
    )

    leadership.sort(
        key=lambda item: item.get("sort_order", 9999)
    )

    service_times = published_only(
        [
            item
            for item in site_data.get("service_times", [])
            if isinstance(item, dict)
        ]
    )

    service_times.sort(
        key=lambda item: item.get("sort_order", 9999)
    )

    social_links = published_only(
        [
            item
            for item in site_data.get("social_links", [])
            if isinstance(item, dict)
        ]
    )

    social_links.sort(
        key=lambda item: item.get("sort_order", 9999)
    )

    ministries = published_only(
        [
            item
            for item in data["ministries"].get("ministries", [])
            if isinstance(item, dict)
        ]
    )

    ministries.sort(
        key=lambda item: item.get("sort_order", 9999)
    )

    programmes = published_only(
        [
            item
            for item in data["programmes"].get("programmes", [])
            if isinstance(item, dict)
        ]
    )

    programmes.sort(
        key=lambda item: item.get("sort_order", 9999)
    )

    sermons = published_only(
        [
            item
            for item in data["sermons"].get("sermons", [])
            if isinstance(item, dict)
        ]
    )

    sermons.sort(
        key=lambda item: (
            item.get("date") or ""
        ),
        reverse=True,
    )

    events = published_only(
        [
            item
            for item in data["events"].get("events", [])
            if isinstance(item, dict)
        ]
    )

    events.sort(
        key=lambda item: item.get("date") or ""
    )

    testimonials = published_only(
        [
            item
            for item in data["testimonials"].get("testimonials", [])
            if isinstance(item, dict)
        ]
    )

    navigation = [
        {
            "name": page["name"],
            "slug": page["slug"] or "home",
            "url": "/" if page["slug"] == "" else f"/{page['slug']}/",
        }
        for page in PAGES
    ]

    return {
        "site": site_data.get("site", {}),
        "leadership": leadership,
        "branches": site_data.get("branches", []),
        "contact": site_data.get("contact", {}),
        "service_times": service_times,
        "location": site_data.get("location", {}),
        "social_links": social_links,
        "livestream": site_data.get("livestream", {}),
        "giving": site_data.get("giving", {}),
        "ministries": ministries,
        "programmes": programmes,
        "sermons": sermons,
        "events": events,
        "testimonials": testimonials,
        "navigation": navigation,
    }


# ============================================================
# JINJA
# ============================================================

def create_environment() -> Environment:

    return Environment(
        loader=FileSystemLoader(
            [
                str(TEMPLATES_DIR),
                str(COMPONENTS_DIR),
            ]
        ),
        autoescape=select_autoescape(
            enabled_extensions=("html", "xml"),
            default_for_string=True,
        ),
        trim_blocks=True,
        lstrip_blocks=True,
    )


# ============================================================
# OUTPUT HELPERS
# ============================================================

def clean_dist() -> None:

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    DIST_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def output_path_for_slug(slug: str) -> Path:

    if slug == "":
        return DIST_DIR / "index.html"

    directory = DIST_DIR / slug
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory / "index.html"


def render_pages(
    environment: Environment,
    shared_context: dict[str, Any],
) -> None:

    for page in PAGES:

        template = environment.get_template(
            page["template"]
        )

        context = {
            **shared_context,
            "current_page": page["slug"] or "home",
            "page_name": page["name"],
        }

        html = template.render(**context)

        output_path = output_path_for_slug(
            page["slug"]
        )

        output_path.write_text(
            html,
            encoding="utf-8",
        )

        print(
            f"GENERATED: "
            f"{output_path.relative_to(PROJECT_ROOT)}"
        )


def copy_assets() -> None:

    if not ASSETS_DIR.exists():
        fail(f"Assets directory not found: {ASSETS_DIR}")

    destination = DIST_DIR / "assets"

    shutil.copytree(
        ASSETS_DIR,
        destination,
        dirs_exist_ok=True,
    )

    print(
        f"COPIED: "
        f"{destination.relative_to(PROJECT_ROOT)}"
    )


# ============================================================
# SUPPORTING FILES
# ============================================================

def resolve_base_url(
    site: dict[str, Any],
) -> str:

    environment_url = os.getenv("SITE_BASE_URL")

    configured_url = site.get("base_url")

    base_url = (
        environment_url
        or configured_url
        or "http://localhost:8000"
    )

    base_url = base_url.rstrip("/")

    if "localhost" in base_url:
        warn(
            "Using development SITE_BASE_URL "
            "'http://localhost:8000'. "
            "Set SITE_BASE_URL before production build."
        )

    return base_url


def generate_sitemap(
    base_url: str,
) -> None:

    urls = []

    for page in PAGES:

        if page["slug"]:
            url = f"{base_url}/{page['slug']}/"
        else:
            url = f"{base_url}/"

        urls.append(url)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for url in urls:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{url}</loc>",
                "  </url>",
            ]
        )

    lines.append("</urlset>")

    path = DIST_DIR / "sitemap.xml"

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print("GENERATED: dist/sitemap.xml")


def generate_robots(base_url: str) -> None:

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )

    path = DIST_DIR / "robots.txt"

    path.write_text(
        content,
        encoding="utf-8",
    )

    print("GENERATED: dist/robots.txt")


def generate_404(
    environment: Environment,
    shared_context: dict[str, Any],
) -> None:

    template = environment.get_template("404.html")

    context = {
        **shared_context,
        "current_page": "404",
        "page_name": "Page Not Found",
    }

    html = template.render(**context)

    path = DIST_DIR / "404.html"

    path.write_text(
        html,
        encoding="utf-8",
    )

    print("GENERATED: dist/404.html")


# ============================================================
# OUTPUT VALIDATION
# ============================================================

def validate_output() -> None:

    expected_files = [
        DIST_DIR / "index.html",
        DIST_DIR / "about" / "index.html",
        DIST_DIR / "ministries" / "index.html",
        DIST_DIR / "sermons" / "index.html",
        DIST_DIR / "programmes" / "index.html",
        DIST_DIR / "events" / "index.html",
        DIST_DIR / "give" / "index.html",
        DIST_DIR / "contact" / "index.html",
        DIST_DIR / "404.html",
        DIST_DIR / "robots.txt",
        DIST_DIR / "sitemap.xml",
        DIST_DIR / "assets" / "css" / "main.css",
        DIST_DIR / "assets" / "css" / "responsive.css",
        DIST_DIR / "assets" / "js" / "main.js",
    ]

    missing = [
        path
        for path in expected_files
        if not path.exists()
    ]

    if missing:
        missing_text = "\n".join(
            f"  - {path.relative_to(PROJECT_ROOT)}"
            for path in missing
        )

        fail(
            "Build completed but expected output "
            f"is missing:\n{missing_text}"
        )


# ============================================================
# WARNING REPORT
# ============================================================

def print_warnings() -> None:

    if not warnings:
        print("\nNo build warnings.")
        return

    print(
        f"\nBUILD WARNINGS ({len(warnings)}):"
    )

    for warning in warnings:
        print(f"  WARNING: {warning}")


# ============================================================
# MAIN BUILD
# ============================================================

def build() -> None:

    print("=" * 60)
    print("Divine River Church - Version 1 Static Build")
    print("=" * 60)

    print("\n1. Loading JSON data...")
    data = load_all_data()

    print("2. Validating source data...")
    validate_all_data(data)

    print("3. Preparing published content...")
    context = prepare_context(data)

    print("4. Cleaning dist/...")
    clean_dist()

    print("5. Initialising Jinja...")
    environment = create_environment()

    print("6. Rendering pages...")
    render_pages(
        environment,
        context,
    )

    print("7. Copying assets...")
    copy_assets()

    print("8. Generating supporting files...")

    base_url = resolve_base_url(
        context["site"]
    )

    generate_404(environment, context)
    generate_sitemap(base_url)
    generate_robots(base_url)

    print("9. Validating generated output...")
    validate_output()

    print_warnings()

    print("\n" + "=" * 60)
    print("BUILD PASSED")
    print("=" * 60)

    print(
        f"\nOutput directory: {DIST_DIR}"
    )


if __name__ == "__main__":

    try:
        build()

    except BuildValidationError as exc:

        print(
            "\nBUILD FAILED",
            file=sys.stderr,
        )

        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )

        sys.exit(1)

    except Exception as exc:

        print(
            "\nBUILD FAILED",
            file=sys.stderr,
        )

        print(
            f"UNEXPECTED ERROR: "
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )

        sys.exit(1)