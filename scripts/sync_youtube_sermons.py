from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import yt_dlp


# ============================================================
# CONFIGURATION
# ============================================================

CHANNEL_STREAMS_URL = (
    "https://www.youtube.com/@divineriverchurch/streams"
)

MIN_DURATION_SECONDS = 48 * 60


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SERMONS_JSON = (
    PROJECT_ROOT
    / "src"
    / "data"
    / "sermons.json"
)

SERMON_IMAGES_DIR = (
    PROJECT_ROOT
    / "src"
    / "assets"
    / "images"
    / "sermons"
)

SERMON_IMAGE_JSON_PREFIX = (
    "assets/images/sermons"
)


# ============================================================
# GENERAL HELPERS
# ============================================================

def format_duration(seconds: int) -> str:
    """
    Convert seconds into HH:MM:SS or MM:SS.
    """

    hours, remainder = divmod(
        seconds,
        3600,
    )

    minutes, secs = divmod(
        remainder,
        60,
    )

    if hours:
        return (
            f"{hours}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )

    return (
        f"{minutes}:"
        f"{secs:02d}"
    )


def normalise_date(
    info: dict[str, Any],
) -> str | None:
    """
    Return a YYYY-MM-DD date.

    Prefer livestream release date, then upload date,
    then available timestamps.
    """

    raw_date = (
        info.get("release_date")
        or info.get("upload_date")
    )

    if (
        isinstance(raw_date, str)
        and len(raw_date) == 8
    ):

        try:

            parsed = datetime.strptime(
                raw_date,
                "%Y%m%d",
            )

            return parsed.strftime(
                "%Y-%m-%d"
            )

        except ValueError:
            pass

    timestamp = (
        info.get("release_timestamp")
        or info.get("timestamp")
    )

    if isinstance(
        timestamp,
        (int, float),
    ):

        return datetime.fromtimestamp(
            timestamp,
            tz=timezone.utc,
        ).date().isoformat()

    return None


def youtube_url(
    video_id: str,
) -> str:

    return (
        "https://www.youtube.com/watch?v="
        f"{video_id}"
    )


def youtube_hq_thumbnail_url(
    video_id: str,
) -> str:

    return (
        "https://i.ytimg.com/vi/"
        f"{video_id}/hqdefault.jpg"
    )


def local_thumbnail_relative_path(
    video_id: str,
) -> str:

    return (
        f"{SERMON_IMAGE_JSON_PREFIX}/"
        f"{video_id}.jpg"
    )


def local_thumbnail_absolute_path(
    video_id: str,
) -> Path:

    return (
        SERMON_IMAGES_DIR
        / f"{video_id}.jpg"
    )


# ============================================================
# LOAD / SAVE SERMONS.JSON
# ============================================================

def load_sermons() -> dict[str, Any]:

    if not SERMONS_JSON.exists():
        raise FileNotFoundError(
            f"sermons.json not found: "
            f"{SERMONS_JSON}"
        )

    with SERMONS_JSON.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(
            file
        )

    if not isinstance(
        data,
        dict,
    ):
        raise ValueError(
            "sermons.json must contain "
            "a JSON object."
        )

    sermons = data.get(
        "sermons"
    )

    if not isinstance(
        sermons,
        list,
    ):
        raise ValueError(
            "sermons.json must contain "
            "a 'sermons' list."
        )

    return data


def save_sermons(
    data: dict[str, Any],
) -> None:

    temporary_path = (
        SERMONS_JSON.with_suffix(
            ".json.tmp"
        )
    )

    with temporary_path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write(
            "\n"
        )

    temporary_path.replace(
        SERMONS_JSON
    )


# ============================================================
# EXISTING SERMON LOOKUP
# ============================================================

def existing_sermon_lookup(
    sermons: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:

    lookup: dict[
        str,
        dict[str, Any],
    ] = {}

    for sermon in sermons:

        if not isinstance(
            sermon,
            dict,
        ):
            continue

        video_id = sermon.get(
            "youtube_id"
        )

        if (
            isinstance(video_id, str)
            and video_id.strip()
        ):
            lookup[
                video_id
            ] = sermon

    return lookup


# ============================================================
# THUMBNAIL DOWNLOAD
# ============================================================

def download_thumbnail(
    video_id: str,
    refresh: bool = False,
) -> tuple[bool, Path]:
    """
    Download a YouTube HQ thumbnail and save it using
    the unique YouTube video ID.

    Example:

    Rh3PJ48RTEI
        ->
    src/assets/images/sermons/Rh3PJ48RTEI.jpg

    Existing thumbnails are not downloaded again unless
    refresh=True.
    """

    SERMON_IMAGES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = (
        local_thumbnail_absolute_path(
            video_id
        )
    )

    if (
        destination.exists()
        and destination.stat().st_size > 0
        and not refresh
    ):

        return (
            False,
            destination,
        )

    thumbnail_url = (
        youtube_hq_thumbnail_url(
            video_id
        )
    )

    request = Request(
        thumbnail_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "DivineRiverChurchWebsite/1.0"
            )
        },
    )

    try:

        with urlopen(
            request,
            timeout=30,
        ) as response:

            image_bytes = (
                response.read()
            )

    except (
        HTTPError,
        URLError,
        TimeoutError,
    ) as exc:

        raise RuntimeError(
            "Could not download thumbnail "
            f"for {video_id}: {exc}"
        ) from exc

    if not image_bytes:
        raise RuntimeError(
            "YouTube returned an empty thumbnail "
            f"for {video_id}."
        )

    temporary_path = (
        destination.with_suffix(
            ".jpg.tmp"
        )
    )

    temporary_path.write_bytes(
        image_bytes
    )

    temporary_path.replace(
        destination
    )

    return (
        True,
        destination,
    )


# ============================================================
# YT-DLP CHANNEL DISCOVERY
# ============================================================

def get_stream_entries(
    max_items: int | None = None,
) -> list[dict[str, Any]]:
    """
    Read the Divine River Church Streams tab.

    This first pass uses lightweight playlist metadata.
    Full metadata is retrieved separately for each video.
    """

    options: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
        "ignoreerrors": True,
    }

    if max_items is not None:
        options[
            "playlistend"
        ] = max_items

    print(
        "\nReading Divine River Church "
        "YouTube Streams..."
    )

    with yt_dlp.YoutubeDL(
        options
    ) as ydl:

        result = (
            ydl.extract_info(
                CHANNEL_STREAMS_URL,
                download=False,
            )
        )

    if not result:
        raise RuntimeError(
            "No channel information "
            "was returned."
        )

    entries = result.get(
        "entries",
        [],
    )

    return [
        entry
        for entry in entries
        if isinstance(
            entry,
            dict,
        )
    ]


def get_full_video_info(
    video_id: str,
) -> dict[str, Any] | None:
    """
    Retrieve full YouTube metadata for one video.

    No video or audio is downloaded.
    """

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "ignoreerrors": True,
        "ignore_no_formats_error": True,
        "retries": 3,
        "socket_timeout": 30,
    }

    with yt_dlp.YoutubeDL(
        options
    ) as ydl:

        info = (
            ydl.extract_info(
                youtube_url(
                    video_id
                ),
                download=False,
            )
        )

    if not isinstance(
        info,
        dict,
    ):
        return None

    return info


# ============================================================
# FINISHED STREAM FILTER
# ============================================================

def is_finished_stream(
    info: dict[str, Any],
) -> bool:
    """
    Only accept livestreams that have completely finished.

    was_live:
        Stream finished and VOD is available.

    post_live:
        Stream ended but YouTube may still be processing it.
        These are skipped until a future sync.
    """

    live_status = info.get(
        "live_status"
    )

    if live_status == "was_live":
        return True

    was_live = info.get(
        "was_live"
    )

    is_live = info.get(
        "is_live"
    )

    return (
        was_live is True
        and is_live is not True
        and live_status != "post_live"
    )


def qualifying_sermon(
    info: dict[str, Any],
    minimum_duration: int,
) -> tuple[bool, str]:

    if not is_finished_stream(
        info
    ):
        return (
            False,
            "not a finished livestream",
        )

    duration = info.get(
        "duration"
    )

    if not isinstance(
        duration,
        (int, float),
    ):
        return (
            False,
            "duration unavailable",
        )

    duration_seconds = int(
        duration
    )

    if (
        duration_seconds
        < minimum_duration
    ):

        return (
            False,
            (
                "duration "
                f"{format_duration(duration_seconds)} "
                "is below minimum"
            ),
        )

    return (
        True,
        "qualifies",
    )


# ============================================================
# SERMON RECORD
# ============================================================

def build_sermon_record(
    info: dict[str, Any],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:

    video_id = str(
        info["id"]
    )

    title = str(
        info.get("title")
        or "Divine River Church Sermon"
    ).strip()

    duration_seconds = int(
        info.get("duration")
        or 0
    )

    date = normalise_date(
        info
    )

    # Preserve manually added fields from an existing record.
    record: dict[str, Any] = (
        dict(existing)
        if existing
        else {}
    )

    record_id = (
        record.get("id")
        or f"youtube-{video_id}"
    )

    record.update(
        {
            "id": record_id,
            "title": title,
            "youtube_id": video_id,
            "youtube_url": youtube_url(
                video_id
            ),

            # IMPORTANT:
            # Store LOCAL website path rather than
            # remote YouTube thumbnail URL.
            "thumbnail": (
                local_thumbnail_relative_path(
                    video_id
                )
            ),

            "duration_seconds": (
                duration_seconds
            ),

            "duration_display": (
                format_duration(
                    duration_seconds
                )
            ),

            "live_status": (
                "was_live"
            ),
        }
    )

    if date:
        record[
            "date"
        ] = date

    if existing is None:

        record[
            "published"
        ] = True

    else:

        record[
            "published"
        ] = existing.get(
            "published",
            True,
        )

    return record


# ============================================================
# SYNC
# ============================================================

def sync_sermons(
    minimum_minutes: int,
    max_items: int | None,
    dry_run: bool,
    refresh_thumbnails: bool,
) -> None:

    minimum_duration = (
        minimum_minutes
        * 60
    )

    SERMON_IMAGES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = load_sermons()

    raw_sermons = data[
        "sermons"
    ]

    sermons: list[
        dict[str, Any]
    ] = [
        sermon
        for sermon in raw_sermons
        if isinstance(
            sermon,
            dict,
        )
    ]

    existing_lookup = (
        existing_sermon_lookup(
            sermons
        )
    )

    entries = get_stream_entries(
        max_items=max_items
    )

    print(
        f"Found {len(entries)} "
        "stream entries."
    )

    print(
        "Minimum sermon duration: "
        f"{minimum_minutes} minutes "
        f"({minimum_duration} seconds)"
    )

    print(
        "Thumbnail directory:"
    )

    print(
        SERMON_IMAGES_DIR
    )

    added = 0
    updated = 0
    skipped = 0
    errors = 0

    thumbnails_downloaded = 0
    thumbnails_existing = 0
    thumbnail_errors = 0

    for index, entry in enumerate(
        entries,
        start=1,
    ):

        video_id = entry.get(
            "id"
        )

        if not video_id:

            skipped += 1

            continue

        video_id = str(
            video_id
        )

        print(
            f"\n[{index}/{len(entries)}] "
            f"{video_id}"
        )

        try:

            info = (
                get_full_video_info(
                    video_id
                )
            )

        except Exception as exc:

            errors += 1

            print(
                "  ERROR retrieving metadata: "
                f"{type(exc).__name__}: "
                f"{exc}"
            )

            continue

        if not info:

            errors += 1

            print(
                "  ERROR: "
                "No full metadata returned."
            )

            continue

        title = (
            info.get("title")
            or video_id
        )

        live_status = (
            info.get(
                "live_status"
            )
        )

        duration = info.get(
            "duration"
        )

        print(
            f"  Title: {title}"
        )

        print(
            "  Live status: "
            f"{live_status}"
        )

        if isinstance(
            duration,
            (int, float),
        ):

            print(
                "  Duration: "
                f"{format_duration(int(duration))}"
            )

        else:

            print(
                "  Duration: unavailable"
            )

        qualifies, reason = (
            qualifying_sermon(
                info,
                minimum_duration,
            )
        )

        if not qualifies:

            skipped += 1

            print(
                f"  SKIPPED: {reason}"
            )

            continue

        # ----------------------------------------------------
        # Download / verify thumbnail
        # ----------------------------------------------------

        thumbnail_path = (
            local_thumbnail_absolute_path(
                video_id
            )
        )

        if dry_run:

            if thumbnail_path.exists():

                print(
                    "  Thumbnail already exists: "
                    f"{thumbnail_path.name}"
                )

            else:

                print(
                    "  DRY RUN thumbnail would download: "
                    f"{thumbnail_path.name}"
                )

        else:

            try:

                downloaded, saved_path = (
                    download_thumbnail(
                        video_id,
                        refresh=(
                            refresh_thumbnails
                        ),
                    )
                )

                if downloaded:

                    thumbnails_downloaded += 1

                    print(
                        "  Thumbnail downloaded: "
                        f"{saved_path.name}"
                    )

                else:

                    thumbnails_existing += 1

                    print(
                        "  Thumbnail already exists: "
                        f"{saved_path.name}"
                    )

            except Exception as exc:

                thumbnail_errors += 1

                print(
                    "  THUMBNAIL ERROR: "
                    f"{exc}"
                )

                # Do not publish a record pointing to a
                # local image that does not exist.
                continue

        # ----------------------------------------------------
        # Build / update sermon record
        # ----------------------------------------------------

        existing = (
            existing_lookup.get(
                video_id
            )
        )

        sermon_record = (
            build_sermon_record(
                info,
                existing,
            )
        )

        if existing is None:

            sermons.append(
                sermon_record
            )

            existing_lookup[
                video_id
            ] = sermon_record

            added += 1

            print(
                "  ADDED"
            )

        else:

            existing.clear()

            existing.update(
                sermon_record
            )

            updated += 1

            print(
                "  UPDATED"
            )

    # --------------------------------------------------------
    # Sort newest first
    # --------------------------------------------------------

    sermons.sort(
        key=lambda sermon: (
            sermon.get("date")
            or ""
        ),
        reverse=True,
    )

    data[
        "sermons"
    ] = sermons

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        "\n"
        + "=" * 60
    )

    print(
        "YOUTUBE SERMON SYNC SUMMARY"
    )

    print(
        "=" * 60
    )

    print(
        f"Added:                 "
        f"{added}"
    )

    print(
        f"Updated:               "
        f"{updated}"
    )

    print(
        f"Skipped:               "
        f"{skipped}"
    )

    print(
        f"Metadata errors:        "
        f"{errors}"
    )

    print(
        f"Thumbnails downloaded:  "
        f"{thumbnails_downloaded}"
    )

    print(
        f"Thumbnails existing:    "
        f"{thumbnails_existing}"
    )

    print(
        f"Thumbnail errors:       "
        f"{thumbnail_errors}"
    )

    print(
        "Total sermons in JSON: "
        f"{len(sermons)}"
    )

    if dry_run:

        print(
            "\nDRY RUN:"
        )

        print(
            "sermons.json was not changed "
            "and no thumbnails were downloaded."
        )

        return

    save_sermons(
        data
    )

    print(
        "\nSaved sermons JSON:"
    )

    print(
        SERMONS_JSON
    )

    print(
        "\nSaved sermon thumbnails:"
    )

    print(
        SERMON_IMAGES_DIR
    )


# ============================================================
# COMMAND LINE
# ============================================================

def parse_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "Sync completed Divine River Church "
            "YouTube livestreams and local thumbnails "
            "into sermons.json."
        )
    )

    parser.add_argument(
        "--min-minutes",
        type=int,
        default=48,
        help=(
            "Minimum livestream duration in minutes. "
            "Default: 48."
        ),
    )

    parser.add_argument(
        "--max-items",
        type=int,
        default=None,
        help=(
            "Only inspect this many entries "
            "from the Streams tab."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Show what would happen without "
            "changing files."
        ),
    )

    parser.add_argument(
        "--refresh-thumbnails",
        action="store_true",
        help=(
            "Download thumbnails again even if "
            "a local thumbnail already exists."
        ),
    )

    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main() -> int:

    args = parse_arguments()

    if args.min_minutes <= 0:

        print(
            "ERROR: --min-minutes must "
            "be greater than 0.",
            file=sys.stderr,
        )

        return 1

    try:

        sync_sermons(
            minimum_minutes=(
                args.min_minutes
            ),
            max_items=(
                args.max_items
            ),
            dry_run=(
                args.dry_run
            ),
            refresh_thumbnails=(
                args.refresh_thumbnails
            ),
        )

    except KeyboardInterrupt:

        print(
            "\nSync cancelled.",
            file=sys.stderr,
        )

        return 130

    except Exception as exc:

        print(
            "\nSYNC FAILED",
            file=sys.stderr,
        )

        print(
            (
                f"{type(exc).__name__}: "
                f"{exc}"
            ),
            file=sys.stderr,
        )

        return 1

    return 0


if __name__ == "__main__":

    raise SystemExit(
        main()
    )