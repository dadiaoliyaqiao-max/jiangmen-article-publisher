#!/usr/bin/env python3
"""Validate a local Jiangmen article publish manifest before browser work."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = {
    "day",
    "date",
    "title",
    "image_count",
    "caption_count",
    "captions",
    "html_path",
    "plain_path",
    "cover_path",
    "first_paragraph",
    "last_paragraph",
}

IMG_RE = re.compile(r"<img\b", re.IGNORECASE)
TAG_RE = re.compile(r"<[^>]+>")
NEGATIVE_PROJECT_RE = re.compile(r"非[^\n]{0,20}(?:项目|现场|实景)")
ROOM_NUMBER_RE = re.compile(r"(?:\d{1,3}\s*栋\s*)?\d{2,4}\s*(?:房|室|号)|(?:房号|室号)\s*[:：]?\s*\d+")


def normalize_text(value: str) -> str:
    value = html.unescape(TAG_RE.sub(" ", value))
    return re.sub(r"\s+", "", value)


def resolve_path(raw: str, manifest_path: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    candidates = [manifest_path.parent / path, Path.cwd() / path]
    return next((candidate for candidate in candidates if candidate.exists()), candidates[0])


def require_int(value: Any, label: str, errors: list[str]) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        errors.append(f"{label} must be a non-negative integer")
        return 0
    return value


def validate_article(article: dict[str, Any], index: int, manifest_path: Path) -> list[str]:
    prefix = f"article {index}"
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - article.keys())
    if missing:
        return [f"{prefix}: missing fields: {', '.join(missing)}"]

    title = str(article["title"]).strip()
    if not title:
        errors.append(f"{prefix}: title is empty")

    try:
        date.fromisoformat(str(article["date"]))
    except ValueError:
        errors.append(f"{prefix}: date must be YYYY-MM-DD")

    image_count = require_int(article["image_count"], f"{prefix}.image_count", errors)
    caption_count = require_int(article["caption_count"], f"{prefix}.caption_count", errors)
    captions = article["captions"]
    if not isinstance(captions, list) or not all(isinstance(item, str) for item in captions):
        errors.append(f"{prefix}: captions must be a list of strings")
        captions = []

    if caption_count != len(captions):
        errors.append(f"{prefix}: caption_count={caption_count}, captions={len(captions)}")
    if image_count != len(captions):
        errors.append(f"{prefix}: image_count={image_count}, captions={len(captions)}")

    for caption_index, caption in enumerate(captions, start=1):
        if NEGATIVE_PROJECT_RE.search(caption):
            errors.append(f"{prefix}: caption {caption_index} contains a negative project disclaimer")
        if ROOM_NUMBER_RE.search(caption):
            errors.append(f"{prefix}: caption {caption_index} contains an exact room number")

    html_path = resolve_path(str(article["html_path"]), manifest_path)
    plain_path = resolve_path(str(article["plain_path"]), manifest_path)
    cover_path = resolve_path(str(article["cover_path"]), manifest_path)
    for label, path in (("html", html_path), ("plain", plain_path), ("cover", cover_path)):
        if not path.is_file():
            errors.append(f"{prefix}: {label} file not found: {path}")

    if html_path.is_file():
        html_text = html_path.read_text(encoding="utf-8")
        actual_images = len(IMG_RE.findall(html_text))
        if actual_images != image_count:
            errors.append(f"{prefix}: HTML images={actual_images}, expected={image_count}")
        normalized_html = normalize_text(html_text)
        for caption_index, caption in enumerate(captions, start=1):
            if normalize_text(f"▲ {caption}") not in normalized_html:
                errors.append(f"{prefix}: caption {caption_index} missing from HTML")
        for field in ("first_paragraph", "last_paragraph"):
            if normalize_text(str(article[field])) not in normalized_html:
                errors.append(f"{prefix}: {field} missing from HTML")

    if plain_path.is_file():
        plain_text = normalize_text(plain_path.read_text(encoding="utf-8"))
        for field in ("first_paragraph", "last_paragraph"):
            if normalize_text(str(article[field])) not in plain_text:
                errors.append(f"{prefix}: {field} missing from plain text")

    if not errors:
        print(f"OK  {index:02d}  {article['date']}  {image_count} images  {title}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path, help="Path to publish-manifest.json")
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read manifest: {exc}", file=sys.stderr)
        return 2

    if not isinstance(payload, list) or not payload:
        print("ERROR: manifest must be a non-empty JSON array", file=sys.stderr)
        return 2

    errors: list[str] = []
    titles: set[str] = set()
    for index, article in enumerate(payload, start=1):
        if not isinstance(article, dict):
            errors.append(f"article {index}: entry must be an object")
            continue
        title = str(article.get("title", "")).strip()
        if title in titles:
            errors.append(f"article {index}: duplicate title: {title}")
        titles.add(title)
        errors.extend(validate_article(article, index, manifest_path))

    if errors:
        for error in errors:
            print(f"ERROR  {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} validation error(s)", file=sys.stderr)
        return 1

    print(f"PASS: {len(payload)} article(s) are ready for platform preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
