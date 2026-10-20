from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime
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
            f"line {exc.lineno}, "
            f"column {exc.colno}: "
            f"{exc.msg}"
        )

    if not isinstance(data, dict):
        fail(
            f"{filename} must contain a JSON object "
            f"at the top level."
        )

    return data


def load_all_data() -> dict[str, dict[str, Any]]:
    return {
        "site": load_json("site.json"),
        "home": load_json("home.json"),
        "about": load_json("about.json"),
        "give": load_json("give.json"),
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
        fail(
            f"{filename} must contain "
            f"top-level key '{key}'."
        )

    value = data[key]

    if not isinstance(value, list):
        fail(
            f"{filename}.{key} must be a list."
        )

    return value


def require_object(
    data: dict[str, Any],
    key: str,
    filename: str,
) -> dict[str, Any]:

    if key not in data:
        fail(
            f"{filename} must contain "
            f"top-level key '{key}'."
        )

    value = data[key]

    if not isinstance(value, dict):
        fail(
            f"{filename}.{key} must be an object."
        )

    return value


def published_only(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Return only explicitly published records.

    A missing 'published' field defaults to unpublished.
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

        if (
            not isinstance(record_id, str)
            or not record_id.strip()
        ):
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

    if (
        not isinstance(value, str)
        or not value.strip()
    ):
        fail(
            f"{description} requires a non-empty "
            f"'{field}' value."
        )

    return value


def validate_optional_string_list(
    value: Any,
    description: str,
) -> None:

    if value is None:
        return

    if not isinstance(value, list):
        fail(
            f"{description} must be a list."
        )

    for item in value:
        if (
            not isinstance(item, str)
            or not item.strip()
        ):
            fail(
                f"{description} must contain only "
                f"non-empty strings."
            )

# ============================================================
# DISPLAY DATE HELPERS
# ============================================================

SERMON_MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def format_sermon_display_date(
    value: str,
    description: str,
) -> str:
    """
    Convert a canonical YYYY-MM-DD sermon date into the
    human-readable form used by the website.

    Example:
        2026-10-04 -> 4 October 2026

    sermons.json remains the canonical source and is not
    modified by the build process.
    """

    try:
        parsed = datetime.strptime(
            value,
            "%Y-%m-%d",
        )

    except ValueError:
        fail(
            f"{description} must use YYYY-MM-DD format. "
            f"Received: {value!r}"
        )

    month_name = SERMON_MONTH_NAMES[
        parsed.month - 1
    ]

    return (
        f"{parsed.day} "
        f"{month_name} "
        f"{parsed.year}"
    )

# ============================================================
# SITE.JSON VALIDATION
# ============================================================

def validate_site_data(
    site_data: dict[str, Any],
) -> None:

    site = require_object(
        site_data,
        "site",
        "site.json",
    )

    # --------------------------------------------------------
    # Core global website information
    # --------------------------------------------------------

    if not site.get("name"):
        warn(
            "site.name has not yet been supplied."
        )

    if not site.get("description"):
        warn(
            "site.description has not yet been supplied."
        )

    if not site.get("logo"):
        warn(
            "site.logo has not yet been supplied."
        )

    # --------------------------------------------------------
    # Contact
    # --------------------------------------------------------

    contact = site_data.get(
        "contact",
        {},
    )

    if not isinstance(contact, dict):
        fail(
            "site.json contact must be an object."
        )

    if not contact.get("phone"):
        warn(
            "No official main church telephone supplied."
        )

    if contact.get("phone_label") is not None:
        require_string(
            contact,
            "phone_label",
            "site.json contact",
        )

    phone_whatsapp_enabled = contact.get(
        "phone_whatsapp_enabled"
    )

    if phone_whatsapp_enabled not in (
        None,
        True,
        False,
    ):
        fail(
            "site.json contact.phone_whatsapp_enabled "
            "must be true, false or null."
        )

    if contact.get("whatsapp") is not None:
        require_string(
            contact,
            "whatsapp",
            "site.json contact",
        )

    # If WhatsApp status has not been confirmed at all,
    # keep the warning. An explicit false value means the
    # absence of WhatsApp is intentional.
    if (
        not contact.get("whatsapp")
        and phone_whatsapp_enabled is None
    ):
        warn(
            "No official church WhatsApp number supplied."
        )

    if not contact.get("email"):
        warn(
            "No official church email supplied."
        )

    if not contact.get("address"):
        warn(
            "No textual church address supplied."
        )

    # --------------------------------------------------------
    # Service times
    # --------------------------------------------------------

    service_times = site_data.get(
        "service_times",
        [],
    )

    if not isinstance(service_times, list):
        fail(
            "site.json service_times must be a list."
        )

    service_dicts = [
        item
        for item in service_times
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        service_dicts,
        "site.json service_times",
    )

    for service in published_only(
        service_dicts
    ):

        service_id = require_string(
            service,
            "id",
            "Published service time",
        )

        require_string(
            service,
            "name",
            f"Service '{service_id}'",
        )

        require_string(
            service,
            "day",
            f"Service '{service_id}'",
        )

        if not (
            service.get("display_time")
            or (
                service.get("start_time")
                and service.get("end_time")
            )
        ):
            fail(
                f"Published service '{service_id}' "
                f"requires display_time or "
                f"start/end times."
            )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location = site_data.get(
        "location",
        {},
    )

    if not isinstance(location, dict):
        fail(
            "site.json location must be an object."
        )

    if not location.get(
        "google_maps_url"
    ):
        warn(
            "Google Maps URL has not yet been supplied."
        )

    # --------------------------------------------------------
    # Social links
    # --------------------------------------------------------

    social_links = site_data.get(
        "social_links",
        [],
    )

    if not isinstance(social_links, list):
        fail(
            "site.json social_links must be a list."
        )

    social_link_dicts = [
        item
        for item in social_links
        if isinstance(item, dict)
    ]

    for link in published_only(
        social_link_dicts
    ):

        require_string(
            link,
            "platform",
            "Published social link",
        )

        require_string(
            link,
            "url",
            (
                "Social link "
                f"'{link.get('platform', 'unknown')}'"
            ),
        )

    # --------------------------------------------------------
    # Livestream
    # --------------------------------------------------------

    livestream = site_data.get(
        "livestream",
        {},
    )

    if not isinstance(livestream, dict):
        fail(
            "site.json livestream must be an object."
        )

    if (
        livestream.get("published") is True
        and not livestream.get(
            "youtube_live_url"
        )
    ):
        warn(
            "Livestream is published but "
            "youtube_live_url is empty."
        )


# ============================================================
# GIVE.JSON VALIDATION
# ============================================================

def validate_give_data(
    give_data: dict[str, Any],
) -> None:

    giving = require_object(
        give_data,
        "giving",
        "give.json",
    )

    # --------------------------------------------------------
    # Introduction
    # --------------------------------------------------------

    if giving.get("introduction") is not None:
        require_string(
            giving,
            "introduction",
            "give.json giving",
        )

    # --------------------------------------------------------
    # Mobile money / direct giving methods
    # --------------------------------------------------------

    giving_methods = giving.get(
        "methods",
        [],
    )

    if not isinstance(giving_methods, list):
        fail(
            "give.json giving.methods must be a list."
        )

    giving_method_dicts = [
        item
        for item in giving_methods
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        giving_method_dicts,
        "give.json giving methods",
    )

    for method in published_only(
        giving_method_dicts
    ):

        method_id = require_string(
            method,
            "id",
            "Published giving method",
        )

        require_string(
            method,
            "name",
            f"Published giving method '{method_id}'",
        )

        require_string(
            method,
            "type",
            f"Published giving method '{method_id}'",
        )

        require_string(
            method,
            "merchant_code",
            f"Published giving method '{method_id}'",
        )

        require_string(
            method,
            "recipient",
            f"Published giving method '{method_id}'",
        )

        require_string(
            method,
            "ussd_code",
            f"Published giving method '{method_id}'",
        )

        if method.get(
            "how_to_give_title"
        ) is not None:
            require_string(
                method,
                "how_to_give_title",
                (
                    "Published giving method "
                    f"'{method_id}'"
                ),
            )

        instructions = method.get(
            "instructions",
            [],
        )

        if (
            not isinstance(instructions, list)
            or not instructions
        ):
            fail(
                "Published giving method "
                f"'{method_id}' requires a non-empty "
                "'instructions' list."
            )

        validate_optional_string_list(
            instructions,
            (
                "Published giving method "
                f"'{method_id}' instructions"
            ),
        )

    # --------------------------------------------------------
    # Bank accounts
    # --------------------------------------------------------

    bank_accounts = giving.get(
        "bank_accounts",
        [],
    )

    if not isinstance(bank_accounts, list):
        fail(
            "give.json giving.bank_accounts "
            "must be a list."
        )

    bank_account_dicts = [
        item
        for item in bank_accounts
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        bank_account_dicts,
        "give.json bank accounts",
    )

    for bank in published_only(
        bank_account_dicts
    ):

        bank_id = require_string(
            bank,
            "id",
            "Published bank account",
        )

        require_string(
            bank,
            "name",
            f"Bank account '{bank_id}'",
        )

        require_string(
            bank,
            "type",
            f"Bank account '{bank_id}'",
        )

        require_string(
            bank,
            "bank_name",
            f"Bank account '{bank_id}'",
        )

        require_string(
            bank,
            "account_name",
            f"Bank account '{bank_id}'",
        )

        require_string(
            bank,
            "account_number",
            f"Bank account '{bank_id}'",
        )

        # ----------------------------------------------------
        # Transfer options
        # ----------------------------------------------------

        transfer_options = bank.get(
            "transfer_options"
        )

        if not isinstance(
            transfer_options,
            dict,
        ):
            fail(
                f"Bank account '{bank_id}' requires "
                "a transfer_options object."
            )

        require_string(
            transfer_options,
            "expand_label",
            (
                f"Bank account '{bank_id}' "
                "transfer options"
            ),
        )

        require_string(
            transfer_options,
            "collapse_label",
            (
                f"Bank account '{bank_id}' "
                "transfer options"
            ),
        )

        show_progress = transfer_options.get(
            "show_progress"
        )

        if show_progress not in (
            True,
            False,
        ):
            fail(
                f"Bank account '{bank_id}' "
                "transfer_options.show_progress "
                "must be true or false."
            )

        routes = transfer_options.get(
            "routes",
            [],
        )

        if (
            not isinstance(routes, list)
            or not routes
        ):
            fail(
                f"Bank account '{bank_id}' requires "
                "at least one transfer route."
            )

        route_dicts = [
            item
            for item in routes
            if isinstance(item, dict)
        ]

        if len(route_dicts) != len(routes):
            fail(
                f"Bank account '{bank_id}' "
                "transfer routes must all be objects."
            )

        check_duplicate_ids(
            route_dicts,
            (
                f"give.json bank account "
                f"'{bank_id}' transfer routes"
            ),
        )

        route_ids: set[str] = set()

        for route in route_dicts:

            route_id = require_string(
                route,
                "id",
                (
                    f"Bank account '{bank_id}' "
                    "transfer route"
                ),
            )

            route_ids.add(route_id)

            require_string(
                route,
                "name",
                (
                    f"Transfer route "
                    f"'{route_id}'"
                ),
            )

            if route.get(
                "how_to_give_title"
            ) is not None:
                require_string(
                    route,
                    "how_to_give_title",
                    (
                        f"Transfer route "
                        f"'{route_id}'"
                    ),
                )

            instructions = route.get(
                "instructions",
                [],
            )

            if (
                not isinstance(instructions, list)
                or not instructions
            ):
                fail(
                    f"Transfer route '{route_id}' "
                    "requires a non-empty "
                    "'instructions' list."
                )

            validate_optional_string_list(
                instructions,
                (
                    f"Transfer route "
                    f"'{route_id}' instructions"
                ),
            )

            navigation = route.get(
                "navigation"
            )

            if not isinstance(
                navigation,
                dict,
            ):
                fail(
                    f"Transfer route '{route_id}' "
                    "requires a navigation object."
                )

            for direction in (
                "previous",
                "next",
            ):

                nav_item = navigation.get(
                    direction
                )

                if nav_item is None:
                    continue

                if not isinstance(
                    nav_item,
                    dict,
                ):
                    fail(
                        f"Transfer route '{route_id}' "
                        f"navigation.{direction} "
                        "must be an object or null."
                    )

                require_string(
                    nav_item,
                    "route_id",
                    (
                        f"Transfer route "
                        f"'{route_id}' "
                        f"navigation.{direction}"
                    ),
                )

                require_string(
                    nav_item,
                    "label",
                    (
                        f"Transfer route "
                        f"'{route_id}' "
                        f"navigation.{direction}"
                    ),
                )

        # ----------------------------------------------------
        # Confirm navigation targets exist
        # ----------------------------------------------------

        for route in route_dicts:

            route_id = route["id"]

            navigation = route.get(
                "navigation",
                {},
            )

            for direction in (
                "previous",
                "next",
            ):

                nav_item = navigation.get(
                    direction
                )

                if nav_item is None:
                    continue

                target_route_id = nav_item.get(
                    "route_id"
                )

                if target_route_id not in route_ids:
                    fail(
                        f"Transfer route '{route_id}' "
                        f"navigation.{direction} "
                        f"references unknown route "
                        f"'{target_route_id}'."
                    )

    # --------------------------------------------------------
    # At least one approved giving option
    # --------------------------------------------------------

    if (
        not giving_method_dicts
        and not bank_account_dicts
    ):
        warn(
            "No giving methods or bank accounts "
            "have yet been supplied."
        )

    # --------------------------------------------------------
    # Safety
    # --------------------------------------------------------

    safety = giving.get(
        "safety",
        [],
    )

    if not isinstance(safety, list):
        fail(
            "give.json giving.safety must be a list."
        )

    validate_optional_string_list(
        safety,
        "give.json giving.safety",
    )

    # --------------------------------------------------------
    # Giving enquiries
    # --------------------------------------------------------

    if giving.get(
        "enquiry_contact"
    ) is not None:
        require_string(
            giving,
            "enquiry_contact",
            "give.json giving",
        )


# ============================================================
# HOME.JSON VALIDATION
# ============================================================

def validate_home_data(
    home_data: dict[str, Any],
) -> None:

    home = require_object(
        home_data,
        "home",
        "home.json",
    )

    expected_sections = [
        "hero",
        "vision_mission",
        "services",
        "sermons",
        "livestream",
        "events",
        "giving",
        "visit",
        "social",
    ]

    for section_name in expected_sections:

        section = home.get(
            section_name
        )

        if not isinstance(
            section,
            dict,
        ):
            fail(
                f"home.json home.{section_name} "
                f"must be an object."
            )

        published = section.get(
            "published"
        )

        if published not in (
            True,
            False,
        ):
            fail(
                f"home.json home.{section_name}."
                f"published must be true or false."
            )

    # --------------------------------------------------------
    # Optional action validation
    # --------------------------------------------------------

    sections_with_actions = [
        "hero",
        "sermons",
        "events",
        "giving",
        "visit",
    ]

    for section_name in sections_with_actions:

        section = home.get(
            section_name,
            {},
        )

        action = (
            section.get("primary_action")
            if section_name == "hero"
            else section.get("action")
        )

        if action is None:
            continue

        if not isinstance(action, dict):
            fail(
                f"home.json home.{section_name} "
                f"action must be an object."
            )

        if action.get("label") is not None:
            require_string(
                action,
                "label",
                (
                    f"home.json "
                    f"home.{section_name} action"
                ),
            )


# ============================================================
# ABOUT.JSON VALIDATION
# ============================================================

def validate_about_data(
    about_data: dict[str, Any],
) -> None:

    about = require_object(
        about_data,
        "about",
        "about.json",
    )

    # --------------------------------------------------------
    # Vision
    # --------------------------------------------------------

    vision = about.get(
        "vision"
    )

    if not isinstance(vision, dict):
        fail(
            "about.json about.vision must be an object."
        )

    require_string(
        vision,
        "title",
        "About vision",
    )

    require_string(
        vision,
        "text",
        "About vision",
    )

    validate_optional_string_list(
    vision.get(
        "scriptures",
        [],
        ),
        "about.json about.vision.scriptures",
    )

    # --------------------------------------------------------
    # Mission
    # --------------------------------------------------------

    mission = about.get(
        "mission"
    )

    if not isinstance(mission, dict):
        fail(
            "about.json about.mission must be an object."
        )

    require_string(
        mission,
        "title",
        "About mission",
    )

    require_string(
        mission,
        "text",
        "About mission",
    )

    validate_optional_string_list(
        mission.get(
            "scriptures",
            [],
        ),
        "about.json about.mission.scriptures",
    )

    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    history = about.get(
        "history"
    )

    if not isinstance(history, dict):
        fail(
            "about.json about.history must be an object."
        )

    require_string(
        history,
        "title",
        "About history",
    )

    require_string(
        history,
        "text",
        "About history",
    )

    # --------------------------------------------------------
    # Statement of faith
    # --------------------------------------------------------

    statement_of_faith = about.get(
        "statement_of_faith"
    )

    if not isinstance(
        statement_of_faith,
        dict,
    ):
        fail(
            "about.json about.statement_of_faith "
            "must be an object."
        )

    require_string(
        statement_of_faith,
        "eyebrow",
        "Statement of faith",
    )

    require_string(
        statement_of_faith,
        "title",
        "Statement of faith",
    )

    require_string(
        statement_of_faith,
        "text",
        "Statement of faith",
    )

    # --------------------------------------------------------
    # Teams section headings
    # --------------------------------------------------------

    teams_section = about.get(
        "teams_section"
    )

    if not isinstance(
        teams_section,
        dict,
    ):
        fail(
            "about.json about.teams_section "
            "must be an object."
        )

    require_string(
        teams_section,
        "eyebrow",
        "About teams section",
    )

    require_string(
        teams_section,
        "title",
        "About teams section",
    )

    # --------------------------------------------------------
    # Values
    # --------------------------------------------------------

    values = about.get(
        "values",
        [],
    )

    if not isinstance(values, list):
        fail(
            "about.json about.values must be a list."
        )

    # --------------------------------------------------------
    # Leadership
    # --------------------------------------------------------

    leadership = about_data.get(
        "leadership",
        [],
    )

    if not isinstance(leadership, list):
        fail(
            "about.json leadership must be a list."
        )

    leadership_dicts = [
        item
        for item in leadership
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        leadership_dicts,
        "about.json leadership",
    )

    for leader in published_only(
        leadership_dicts
    ):

        require_string(
            leader,
            "id",
            "Published leadership record",
        )

        require_string(
            leader,
            "name",
            "Published leadership record",
        )

    # --------------------------------------------------------
    # Teams
    # --------------------------------------------------------

    teams = about_data.get(
        "teams",
        [],
    )

    if not isinstance(teams, list):
        fail(
            "about.json teams must be a list."
        )

    team_dicts = [
        item
        for item in teams
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        team_dicts,
        "about.json teams",
    )

    for team in published_only(
        team_dicts
    ):

        team_id = require_string(
            team,
            "id",
            "Published team",
        )

        require_string(
            team,
            "name",
            f"Published team '{team_id}'",
        )

        require_string(
            team,
            "description",
            f"Published team '{team_id}'",
        )

    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    branches = about_data.get(
        "branches",
        [],
    )

    if not isinstance(branches, list):
        fail(
            "about.json branches must be a list."
        )


# ============================================================
# MINISTRIES.JSON VALIDATION
# ============================================================

def validate_ministries(
    data: dict[str, Any],
) -> None:

    ministries = require_list(
        data,
        "ministries",
        "ministries.json",
    )

    records = [
        item
        for item in ministries
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        records,
        "ministries.json",
    )

    if not records:
        warn(
            "ministries.json currently contains "
            "no ministries."
        )

    for ministry in published_only(
        records
    ):

        ministry_id = require_string(
            ministry,
            "id",
            "Published ministry",
        )

        require_string(
            ministry,
            "name",
            f"Published ministry '{ministry_id}'",
        )

        require_string(
            ministry,
            "summary",
            f"Published ministry '{ministry_id}'",
        )

        require_string(
            ministry,
            "details",
            f"Published ministry '{ministry_id}'",
        )

        scriptures = ministry.get(
            "scriptures",
            [],
        )

        validate_optional_string_list(
            scriptures,
            (
                f"Ministry '{ministry_id}' "
                "scriptures"
            ),
        )


# ============================================================
# PROGRAMMES.JSON VALIDATION
# ============================================================

def validate_programmes(
    data: dict[str, Any],
) -> None:

    programmes = require_list(
        data,
        "programmes",
        "programmes.json",
    )

    records = [
        item
        for item in programmes
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        records,
        "programmes.json",
    )

    if not records:
        warn(
            "programmes.json currently contains "
            "no programmes."
        )

    for programme in published_only(
        records
    ):

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
                f"Published programme "
                f"'{programme_id}' requires "
                f"display_time or start/end times."
            )


# ============================================================
# SERMONS.JSON VALIDATION
# ============================================================

def validate_sermons(
    data: dict[str, Any],
) -> None:

    sermons = require_list(
        data,
        "sermons",
        "sermons.json",
    )

    records = [
        item
        for item in sermons
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        records,
        "sermons.json",
    )

    if not records:
        warn(
            "sermons.json currently contains "
            "no sermons."
        )

    for sermon in published_only(
        records
    ):

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

        sermon_date = require_string(
            sermon,
            "date",
            f"Sermon '{sermon_id}'",
        )

        # Confirm that the canonical YouTube date can be
        # converted into the website display format.
        format_sermon_display_date(
            sermon_date,
            f"Sermon '{sermon_id}' date",
        )

        require_string(
            sermon,
            "thumbnail",
            f"Sermon '{sermon_id}'",
        )

        require_string(
            sermon,
            "duration_display",
            f"Sermon '{sermon_id}'",
        )

        if not (
            sermon.get("youtube_id")
            or sermon.get("youtube_url")
        ):
            fail(
                f"Published sermon "
                f"'{sermon_id}' requires "
                f"youtube_id or youtube_url."
            )


# ============================================================
# EVENTS.JSON VALIDATION
# ============================================================

def validate_events(
    data: dict[str, Any],
) -> None:

    events = require_list(
        data,
        "events",
        "events.json",
    )

    records = [
        item
        for item in events
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        records,
        "events.json",
    )

    if not records:
        warn(
            "events.json currently contains "
            "no events."
        )

    for event in published_only(
        records
    ):

        event_id = require_string(
            event,
            "id",
            "Published event",
        )

        # ----------------------------------------------------
        # Core event information
        # ----------------------------------------------------

        require_string(
            event,
            "title",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "summary",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "date",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "display_date",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "start_time",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "display_time",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "venue",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "venue_short",
            f"Event '{event_id}'",
        )

        require_string(
            event,
            "admission",
            f"Event '{event_id}'",
        )

        # ----------------------------------------------------
        # Full description
        # ----------------------------------------------------

        description = event.get(
            "description",
            [],
        )

        if (
            not isinstance(description, list)
            or not description
        ):
            fail(
                f"Event '{event_id}' requires "
                "a non-empty description list."
            )

        validate_optional_string_list(
            description,
            (
                f"Event '{event_id}' "
                "description"
            ),
        )

        # ----------------------------------------------------
        # Featuring
        # ----------------------------------------------------

        featuring = event.get(
            "featuring",
            [],
        )

        if not isinstance(
            featuring,
            list,
        ):
            fail(
                f"Event '{event_id}' "
                "featuring must be a list."
            )

        validate_optional_string_list(
            featuring,
            (
                f"Event '{event_id}' "
                "featuring"
            ),
        )

        # ----------------------------------------------------
        # Media
        # ----------------------------------------------------

        media = event.get(
            "media"
        )

        if not isinstance(
            media,
            dict,
        ):
            fail(
                f"Event '{event_id}' requires "
                "a media object."
            )

        poster = require_string(
            media,
            "poster",
            (
                f"Event '{event_id}' "
                "media"
            ),
        )

        require_string(
            media,
            "poster_alt",
            (
                f"Event '{event_id}' "
                "media"
            ),
        )

        # Confirm main poster exists in src/
        poster_path = (
            SRC_DIR
            / poster
        )

        if not poster_path.exists():
            fail(
                f"Event '{event_id}' poster "
                f"does not exist: {poster}"
            )

        gallery = media.get(
            "gallery",
            [],
        )

        if not isinstance(
            gallery,
            list,
        ):
            fail(
                f"Event '{event_id}' "
                "media.gallery must be a list."
            )

        for index, gallery_item in enumerate(
            gallery,
            start=1,
        ):

            if not isinstance(
                gallery_item,
                dict,
            ):
                fail(
                    f"Event '{event_id}' "
                    f"gallery item {index} "
                    "must be an object."
                )

            gallery_image = require_string(
                gallery_item,
                "image",
                (
                    f"Event '{event_id}' "
                    f"gallery item {index}"
                ),
            )

            require_string(
                gallery_item,
                "alt",
                (
                    f"Event '{event_id}' "
                    f"gallery item {index}"
                ),
            )

            gallery_path = (
                SRC_DIR
                / gallery_image
            )

            if not gallery_path.exists():
                fail(
                    f"Event '{event_id}' "
                    f"gallery image does not exist: "
                    f"{gallery_image}"
                )

        # ----------------------------------------------------
        # External links
        # ----------------------------------------------------

        external_links = event.get(
            "external_links",
            {},
        )

        if not isinstance(
            external_links,
            dict,
        ):
            fail(
                f"Event '{event_id}' "
                "external_links must be an object."
            )

        for platform, link in (
            external_links.items()
        ):

            if not isinstance(
                link,
                dict,
            ):
                fail(
                    f"Event '{event_id}' "
                    f"external link '{platform}' "
                    "must be an object."
                )

            require_string(
                link,
                "label",
                (
                    f"Event '{event_id}' "
                    f"external link '{platform}'"
                ),
            )

            require_string(
                link,
                "url",
                (
                    f"Event '{event_id}' "
                    f"external link '{platform}'"
                ),
            )

        # ----------------------------------------------------
        # Shared site-link flags
        # ----------------------------------------------------

        for flag_name in (
            "use_site_youtube",
            "use_site_facebook",
            "use_site_directions",
        ):

            flag_value = event.get(
                flag_name
            )

            if flag_value not in (
                True,
                False,
            ):
                fail(
                    f"Event '{event_id}' "
                    f"{flag_name} must be "
                    "true or false."
                )

        # ----------------------------------------------------
        # Optional sort order
        # ----------------------------------------------------

        sort_order = event.get(
            "sort_order"
        )

        if (
            sort_order is not None
            and not isinstance(
                sort_order,
                int,
            )
        ):
            fail(
                f"Event '{event_id}' "
                "sort_order must be an integer."
            )


# ============================================================
# TESTIMONIALS.JSON VALIDATION
# ============================================================

def validate_testimonials(
    data: dict[str, Any],
) -> None:

    testimonials = require_list(
        data,
        "testimonials",
        "testimonials.json",
    )

    records = [
        item
        for item in testimonials
        if isinstance(item, dict)
    ]

    check_duplicate_ids(
        records,
        "testimonials.json",
    )

    for testimonial in published_only(
        records
    ):

        testimonial_id = require_string(
            testimonial,
            "id",
            "Published testimonial",
        )

        if (
            testimonial.get(
                "permission_confirmed"
            )
            is not True
        ):
            fail(
                f"Published testimonial "
                f"'{testimonial_id}' does not have "
                f"publication permission."
            )

        require_string(
            testimonial,
            "text",
            f"Testimonial '{testimonial_id}'",
        )


# ============================================================
# VALIDATE ALL SOURCE DATA
# ============================================================

def validate_all_data(
    data: dict[str, dict[str, Any]],
) -> None:

    validate_site_data(
        data["site"]
    )

    validate_home_data(
        data["home"]
    )

    validate_about_data(
        data["about"]
    )

    validate_give_data(
        data["give"]
    )

    validate_ministries(
        data["ministries"]
    )

    validate_programmes(
        data["programmes"]
    )

    validate_sermons(
        data["sermons"]
    )

    validate_events(
        data["events"]
    )

    validate_testimonials(
        data["testimonials"]
    )


# ============================================================
# PREPARE TEMPLATE DATA
# ============================================================

def prepare_context(
    data: dict[str, dict[str, Any]],
) -> dict[str, Any]:

    site_data = data["site"]
    home_data = data["home"]
    about_data = data["about"]
    give_data = data["give"]

    # --------------------------------------------------------
    # Home configuration
    # --------------------------------------------------------

    home = home_data.get(
        "home",
        {},
    )

    # --------------------------------------------------------
    # About institutional content
    # --------------------------------------------------------

    about = about_data.get(
        "about",
        {},
    )

    # --------------------------------------------------------
    # Giving content
    # --------------------------------------------------------

    giving = give_data.get(
        "giving",
        {},
    )

    # --------------------------------------------------------
    # Leadership
    # --------------------------------------------------------

    leadership = published_only(
        [
            item
            for item in about_data.get(
                "leadership",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    leadership.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

    # --------------------------------------------------------
    # Teams
    # --------------------------------------------------------

    teams = published_only(
        [
            item
            for item in about_data.get(
                "teams",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    teams.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    branches = [
        item
        for item in about_data.get(
            "branches",
            [],
        )
        if isinstance(item, dict)
    ]

    branches.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

    # --------------------------------------------------------
    # Service times
    # --------------------------------------------------------

    service_times = published_only(
        [
            item
            for item in site_data.get(
                "service_times",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    service_times.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

    # --------------------------------------------------------
    # Social links
    # --------------------------------------------------------

    social_links = published_only(
        [
            item
            for item in site_data.get(
                "social_links",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    social_links.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

    # --------------------------------------------------------
    # Ministries
    # --------------------------------------------------------

    ministries = published_only(
        [
            item
            for item in data["ministries"].get(
                "ministries",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    ministries.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

    # --------------------------------------------------------
    # Programmes
    # --------------------------------------------------------

    programmes = published_only(
        [
            item
            for item in data["programmes"].get(
                "programmes",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    programmes.sort(
        key=lambda item: item.get(
            "sort_order",
            9999,
        )
    )

        # --------------------------------------------------------
    # Sermons
    # --------------------------------------------------------

    sermons = published_only(
        [
            dict(item)
            for item in data["sermons"].get(
                "sermons",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    # --------------------------------------------------------
    # Sermon presentation data
    # --------------------------------------------------------
    #
    # sermons.json remains the canonical source:
    #
    #     "date": "2026-10-04"
    #
    # The build adds a presentation-only value:
    #
    #     "display_date": "4 October 2026"
    #
    # Because each sermon is copied above with dict(item),
    # the source JSON data is not modified.
    # --------------------------------------------------------

    for sermon in sermons:

        sermon_id = sermon.get(
            "id",
            "unknown",
        )

        sermon["display_date"] = (
            format_sermon_display_date(
                sermon["date"],
                f"Sermon '{sermon_id}' date",
            )
        )

    # Newest sermon first.
    sermons.sort(
        key=lambda item: (
            item.get("date")
            or ""
        ),
        reverse=True,
    )

    # --------------------------------------------------------
    # Events
    # --------------------------------------------------------

    events = published_only(
        [
            item
            for item in data["events"].get(
                "events",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    events.sort(
        key=lambda item: (
            item.get("date")
            or ""
        )
    )

    # --------------------------------------------------------
    # Testimonials
    # --------------------------------------------------------

    testimonials = published_only(
        [
            item
            for item in data[
                "testimonials"
            ].get(
                "testimonials",
                [],
            )
            if isinstance(item, dict)
        ]
    )

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    navigation = [
        {
            "name": page["name"],
            "slug": (
                page["slug"]
                or "home"
            ),
            "url": (
                "/"
                if page["slug"] == ""
                else f"/{page['slug']}/"
            ),
        }
        for page in PAGES
    ]

    # --------------------------------------------------------
    # Shared template context
    # --------------------------------------------------------

    return {
        # Global site information
        "site": site_data.get(
            "site",
            {},
        ),

        # Home-page configuration
        "home": home,

        # About-page institutional information
        "about": about,

        # About-page collections
        "leadership": leadership,
        "teams": teams,
        "branches": branches,

        # Global site collections/configuration
        "contact": site_data.get(
            "contact",
            {},
        ),
        "service_times": service_times,
        "location": site_data.get(
            "location",
            {},
        ),
        "social_links": social_links,
        "livestream": site_data.get(
            "livestream",
            {},
        ),

        # Give-page content
        "giving": giving,

        # Content collections
        "ministries": ministries,
        "programmes": programmes,
        "sermons": sermons,
        "events": events,
        "testimonials": testimonials,

        # Navigation
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
            enabled_extensions=(
                "html",
                "xml",
            ),
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
        shutil.rmtree(
            DIST_DIR
        )

    DIST_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


def output_path_for_slug(
    slug: str,
) -> Path:

    if slug == "":
        return (
            DIST_DIR
            / "index.html"
        )

    directory = (
        DIST_DIR
        / slug
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return (
        directory
        / "index.html"
    )


def render_pages(
    environment: Environment,
    shared_context: dict[str, Any],
) -> None:

    for page in PAGES:

        template = (
            environment.get_template(
                page["template"]
            )
        )

        context = {
            **shared_context,
            "current_page": (
                page["slug"]
                or "home"
            ),
            "page_name": page["name"],
        }

        html = template.render(
            **context
        )

        output_path = (
            output_path_for_slug(
                page["slug"]
            )
        )

        output_path.write_text(
            html,
            encoding="utf-8",
        )

        print(
            "GENERATED: "
            f"{output_path.relative_to(PROJECT_ROOT)}"
        )


def copy_assets() -> None:

    if not ASSETS_DIR.exists():
        fail(
            f"Assets directory not found: "
            f"{ASSETS_DIR}"
        )

    destination = (
        DIST_DIR
        / "assets"
    )

    shutil.copytree(
        ASSETS_DIR,
        destination,
        dirs_exist_ok=True,
    )

    print(
        "COPIED: "
        f"{destination.relative_to(PROJECT_ROOT)}"
    )


# ============================================================
# SUPPORTING FILES
# ============================================================

def resolve_base_url(
    site: dict[str, Any],
) -> str:

    environment_url = os.getenv(
        "SITE_BASE_URL"
    )

    configured_url = site.get(
        "base_url"
    )

    base_url = (
        environment_url
        or configured_url
        or "http://localhost:8000"
    )

    base_url = base_url.rstrip(
        "/"
    )

    if "localhost" in base_url:
        warn(
            "Using development SITE_BASE_URL "
            "'http://localhost:8000'. "
            "Set SITE_BASE_URL before "
            "production build."
        )

    return base_url


def generate_sitemap(
    base_url: str,
) -> None:

    urls: list[str] = []

    for page in PAGES:

        if page["slug"]:
            url = (
                f"{base_url}/"
                f"{page['slug']}/"
            )
        else:
            url = (
                f"{base_url}/"
            )

        urls.append(url)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<urlset '
            'xmlns="http://www.sitemaps.org/'
            'schemas/sitemap/0.9">'
        ),
    ]

    for url in urls:
        lines.extend(
            [
                "  <url>",
                f"    <loc>{url}</loc>",
                "  </url>",
            ]
        )

    lines.append(
        "</urlset>"
    )

    path = (
        DIST_DIR
        / "sitemap.xml"
    )

    path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    print(
        "GENERATED: dist/sitemap.xml"
    )


def generate_robots(
    base_url: str,
) -> None:

    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {base_url}/sitemap.xml\n"
    )

    path = (
        DIST_DIR
        / "robots.txt"
    )

    path.write_text(
        content,
        encoding="utf-8",
    )

    print(
        "GENERATED: dist/robots.txt"
    )


def generate_404(
    environment: Environment,
    shared_context: dict[str, Any],
) -> None:

    template = (
        environment.get_template(
            "404.html"
        )
    )

    context = {
        **shared_context,
        "current_page": "404",
        "page_name": "Page Not Found",
    }

    html = template.render(
        **context
    )

    path = (
        DIST_DIR
        / "404.html"
    )

    path.write_text(
        html,
        encoding="utf-8",
    )

    print(
        "GENERATED: dist/404.html"
    )


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
            (
                "  - "
                f"{path.relative_to(PROJECT_ROOT)}"
            )
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
        print(
            "\nNo build warnings."
        )
        return

    print(
        f"\nBUILD WARNINGS "
        f"({len(warnings)}):"
    )

    for warning in warnings:
        print(
            f"  WARNING: {warning}"
        )


# ============================================================
# MAIN BUILD
# ============================================================

def build() -> None:

    # Prevent duplicate warnings if build() is called
    # more than once in the same Python process.
    warnings.clear()

    print(
        "=" * 60
    )

    print(
        "Divine River Church - "
        "Version 1 Static Build"
    )

    print(
        "=" * 60
    )

    print(
        "\n1. Loading JSON data..."
    )

    data = load_all_data()

    print(
        "2. Validating source data..."
    )

    validate_all_data(
        data
    )

    print(
        "3. Preparing published content..."
    )

    context = prepare_context(
        data
    )

    print(
        "4. Cleaning dist/..."
    )

    clean_dist()

    print(
        "5. Initialising Jinja..."
    )

    environment = (
        create_environment()
    )

    print(
        "6. Rendering pages..."
    )

    render_pages(
        environment,
        context,
    )

    print(
        "7. Copying assets..."
    )

    copy_assets()

    print(
        "8. Generating supporting files..."
    )

    base_url = resolve_base_url(
        context["site"]
    )

    generate_404(
        environment,
        context,
    )

    generate_sitemap(
        base_url
    )

    generate_robots(
        base_url
    )

    print(
        "9. Validating generated output..."
    )

    validate_output()

    print_warnings()

    print(
        "\n" + "=" * 60
    )

    print(
        "BUILD PASSED"
    )

    print(
        "=" * 60
    )

    print(
        f"\nOutput directory: "
        f"{DIST_DIR}"
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
            (
                "UNEXPECTED ERROR: "
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
            file=sys.stderr,
        )

        sys.exit(1)