#!/usr/bin/env python3
"""Strip WordPress runtime markup that breaks once the backend is gone.

Three categories handled in one pass over every HTML file under
`output_dir`:

1. **Comment forms**: `<div id="respond">…</div><!-- #respond -->` blocks.
2. **Comment-reply links**: both block-theme variant
   (`<div class="wp-block-comment-reply-link">…</div>`) and classic-theme
   variant (`<a class="comment-reply-link">…</a>` inside any wrapper). The
   matching is structural — link text doesn't matter.
3. **Dead `<head>` tags and scripts**: REST API discovery, RSD, oEmbed
   alternates, RSS alternates, archive `next` links, and the
   `comment-reply-js` script tag whose target file we also delete.

The corresponding asset `wp-includes/js/comment-reply.min.js` is removed
after script tags are stripped, since nothing references it anymore.

Usage:
    strip-wp-runtime.py <output_dir>
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

RESPOND = re.compile(
    r'<div id="respond"[^>]*>.*?</div><!--\s*#respond\s*-->',
    re.DOTALL,
)
REPLY_LINK_BLOCK = re.compile(
    r'<div class="wp-block-comment-reply-link">.*?</div>\s*',
    re.DOTALL,
)
REPLY_LINK_CLASSIC = re.compile(
    r'<a [^>]*class="[^"]*comment-reply-link[^"]*"[^>]*>[^<]*</a>',
)
COMMENT_REPLY_SCRIPT = re.compile(
    r'\s*<script[^>]*id="comment-reply-js"[^>]*></script>\n?',
)

DROP_HEAD = [
    re.compile(p)
    for p in (
        r'<link rel="https://api\.w\.org/"[^>]*/>',
        r'<link rel="EditURI"[^>]*/>',
        r'<link rel="alternate" title="JSON"[^>]*/>',
        r'<link rel="alternate" title="oEmbed[^"]*"[^>]*/>',
        r"<link rel='shortlink'[^>]*/>",
        r'<link rel="alternate" type="application/rss\+xml"[^>]*/>',
        r'<link rel="next" href="https?://[^"]+/page/\d+/"[^>]*/>',
    )
]


def strip(html: str) -> str:
    html = RESPOND.sub('', html)
    html = REPLY_LINK_BLOCK.sub('', html)
    html = REPLY_LINK_CLASSIC.sub('', html)
    html = COMMENT_REPLY_SCRIPT.sub('', html)
    for pattern in DROP_HEAD:
        html = pattern.sub('', html)
    return html


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_dir', type=pathlib.Path)
    args = parser.parse_args()

    if not args.output_dir.is_dir():
        print(f'output_dir not found: {args.output_dir}', file=sys.stderr)
        return 1

    changed = 0
    for path in args.output_dir.rglob('*.html'):
        original = path.read_text(encoding='utf-8')
        new = strip(original)
        if new != original:
            path.write_text(new, encoding='utf-8')
            changed += 1

    reply_js = args.output_dir / 'wp-includes' / 'js' / 'comment-reply.min.js'
    if reply_js.exists():
        reply_js.unlink()
        print(f'removed {reply_js.relative_to(args.output_dir)}')
    print(f'stripped runtime markup from {changed} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
