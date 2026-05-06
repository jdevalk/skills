#!/usr/bin/env python3
"""Insert a banner HTML comment after `<!DOCTYPE html>` in every page.

Brands the output as a static clone so future maintainers (or anyone reading
view-source) can tell at a glance that this isn't the live WP install.
Idempotent: skips pages that already contain the banner.

Usage:
    insert-banner.py <output_dir> [--message "..."]
"""

from __future__ import annotations

import argparse
import pathlib
import sys

DOCTYPE = '<!DOCTYPE html>'
DEFAULT_MESSAGE = (
    'Static site generated from a WordPress source — no live WP backend.'
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_dir', type=pathlib.Path)
    parser.add_argument(
        '--message',
        default=DEFAULT_MESSAGE,
        help='Banner text to embed in the comment.',
    )
    args = parser.parse_args()

    if not args.output_dir.is_dir():
        print(f'output_dir not found: {args.output_dir}', file=sys.stderr)
        return 1

    banner = f'<!-- {args.message} -->'
    inserted = 0
    for path in args.output_dir.rglob('*.html'):
        if '.git' in path.parts:
            continue
        text = path.read_text(encoding='utf-8')
        if banner in text or not text.startswith(DOCTYPE):
            continue
        path.write_text(text.replace(DOCTYPE, DOCTYPE + '\n' + banner, 1), encoding='utf-8')
        inserted += 1
    print(f'banner inserted in {inserted} files')
    return 0


if __name__ == '__main__':
    sys.exit(main())
