#!/usr/bin/env python3
"""Create the ignored local workspace and a safe manifest starter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DIRECTORIES = (
    "manuscripts",
    "images",
    "working",
    "progress",
)

MANIFEST_EXAMPLE = [
    {
        "day": 1,
        "date": "2026-01-01",
        "title": "替换为审核通过的文章标题",
        "image_count": 1,
        "caption_count": 1,
        "captions": ["替换为准确的图片内容说明"],
        "html_path": "local-data/working/article-01.html",
        "plain_path": "local-data/working/article-01.txt",
        "cover_path": "local-data/images/approved-text-free-cover.jpg",
        "first_paragraph": "替换为正文第一段",
        "last_paragraph": "替换为正文最后一段",
    }
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("local-data"),
        help="Ignored local workspace root (default: local-data)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    for name in DIRECTORIES:
        (root / name).mkdir(parents=True, exist_ok=True)

    example = root / "publish-manifest.example.json"
    if example.exists():
        print(f"KEEP {example}")
    else:
        example.write_text(
            json.dumps(MANIFEST_EXAMPLE, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"CREATE {example}")

    print(f"READY {root}")
    print("Copy the example to publish-manifest.json, fill every field, then run the validator.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
