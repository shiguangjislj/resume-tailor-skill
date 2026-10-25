#!/usr/bin/env python3
"""Read-only formatting checks for ONE experience body; standard library only."""
import argparse
import html
import json
from pathlib import Path
import re

HAN = r"\u3400-\u4dbf\u4e00-\u9fff"
BOUNDARY = re.compile(rf"[{HAN}][ \t\u00a0]+[A-Za-z0-9]|[A-Za-z0-9][ \t\u00a0]+[{HAN}]")


def visible_text(text):
    # Ignore code and URL targets; put literal paths in backticks. Never mutate input.
    text = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "\n", text)
    text = re.sub(r"`[^`\n]+`", "◇", text)
    text = re.sub(r"\[([^\]]+)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"https?://[^\s<>]+", "◇", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"(?m)^\s*[-*+]\s+", "", text)
    return text


def inspect(text, max_paragraphs=4, max_chars=None):
    visible = visible_text(text)
    paragraphs = [p for p in re.split(r"\n\s*\n", visible.strip()) if p.strip()]
    chars = len(re.sub(r"\s", "", visible))
    errors = []
    if not paragraphs:
        errors.append({"kind": "empty", "message": "正文为空"})
    if max_paragraphs is not None and len(paragraphs) > max_paragraphs:
        errors.append({"kind": "paragraphs", "actual": len(paragraphs), "limit": max_paragraphs})
    if max_chars is not None and chars > max_chars:
        errors.append({"kind": "characters", "actual": chars, "limit": max_chars})
    for n, line in enumerate(visible.splitlines(), 1):
        matches = [m.group(0) for m in BOUNDARY.finditer(line)]
        if matches:
            errors.append({"kind": "spacing", "line": n, "matches": matches})
    return {"paragraphs": len(paragraphs), "visible_characters": chars,
            "errors": errors, "ok": not errors,
            "scope": "仅检查单段经历正文的常见文本格式；不验证事实、语义、复杂标记或视觉布局"}


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("body_file", type=Path)
    parser.add_argument("--max-paragraphs", type=positive, default=4)
    parser.add_argument("--max-chars", type=positive)
    args = parser.parse_args()
    try:
        body = args.body_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f"Cannot read input: {exc}\n")
    result = inspect(body, args.max_paragraphs, args.max_chars)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
