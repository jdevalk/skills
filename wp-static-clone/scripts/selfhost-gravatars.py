#!/usr/bin/env python3
"""Download every Gravatar referenced in scraped HTML and rewrite to local.

Each Gravatar request from the live site leaks the visitor's IP to a third
party and adds a render-blocking external load per avatar. Self-hosting
fixes both, and turns the archive into a self-contained bundle.

Detection notes:
- Both `&` and `&#038;` (HTML-encoded) appear in attribute values, so the
  regex tolerates either between query parameters.
- The same hash often appears at multiple sizes (`?s=40`, `?s=80` for
  retina). Each is a separate file.
- The extension is detected from response bytes, not the URL — Gravatar
  serves JPEG for real avatars and PNG for the `d=mm` mystery-man
  fallback. A wrong extension breaks the served Content-Type.

Usage:
    selfhost-gravatars.py <output_dir>
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import urllib.request

URL_RE = re.compile(
    r'https?://(?:secure\.)?gravatar\.com/avatar/'
    r'(?P<hash>[a-fA-F0-9]+)\?[^"\'\s>]*?s=(?P<size>\d+)[^"\'\s>]*'
)


def detect_ext(blob: bytes) -> str:
    if blob.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'png'
    if blob.startswith(b'\xff\xd8\xff'):
        return 'jpg'
    if blob.startswith(b'GIF8'):
        return 'gif'
    if blob[:4] == b'RIFF' and blob[8:12] == b'WEBP':
        return 'webp'
    return 'bin'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_dir', type=pathlib.Path)
    args = parser.parse_args()

    root = args.output_dir
    if not root.is_dir():
        print(f'output_dir not found: {root}', file=sys.stderr)
        return 1

    avatars = root / 'avatars'
    avatars.mkdir(exist_ok=True)

    pairs: set[tuple[str, str]] = set()
    for path in root.rglob('*.html'):
        if '.git' in path.parts:
            continue
        for match in URL_RE.finditer(path.read_text(encoding='utf-8')):
            pairs.add((match['hash'], match['size']))

    local: dict[tuple[str, str], str] = {}
    for h, s in sorted(pairs):
        url = f'https://secure.gravatar.com/avatar/{h}?s={s}&d=mm&r=g'
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        blob = urllib.request.urlopen(request).read()
        out = avatars / f'{h}-{s}.{detect_ext(blob)}'
        out.write_bytes(blob)
        local[(h, s)] = '/' + str(out.relative_to(root))

    def replace(match: re.Match[str]) -> str:
        return local.get((match['hash'], match['size']), match.group(0))

    rewritten = 0
    for path in root.rglob('*.html'):
        if '.git' in path.parts:
            continue
        original = path.read_text(encoding='utf-8')
        new = URL_RE.sub(replace, original)
        if new != original:
            path.write_text(new, encoding='utf-8')
            rewritten += 1

    print(f'downloaded {len(local)} avatars, rewrote {rewritten} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
