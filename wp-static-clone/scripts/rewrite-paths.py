#!/usr/bin/env python3
"""Rewrite asset and page links in scraped HTML to be root-relative.

`wget -k` produces a mix of `../wp-content/...` (depth-relative) and bare
`wp-content/...` (homepage). Both work locally but break the moment a page
moves. This pass converts both forms — plus srcset entries and inter-page
links — to root-relative `/wp-content/...` and `/<slug>/`.

Usage:
    rewrite-paths.py <output_dir> <urls.txt> [--source-domain example.com]

The page-slug list is derived from `urls.txt`, not from a directory walk —
otherwise wget-grabbed archive directories like `category/`, `feed/`,
`author/`, `wp-json/` get wrongly classified as pages.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOTS = {'wp-content', 'wp-includes'}
ATTRS = r'(?:href|src|content|action|data-src|data-href)'


def page_slugs_from_urls(urls_file: pathlib.Path) -> list[str]:
    """Return the list of top-level page slugs from the sitemap URL list.

    A slug is the first path segment of any URL that has at least one
    segment. Homepage (`/`) yields no slug. Multi-segment URLs contribute
    only their first segment, since wget collapses them under that
    directory.
    """
    slugs: set[str] = set()
    for line in urls_file.read_text(encoding='utf-8').splitlines():
        url = line.strip()
        if not url or url.startswith('#'):
            continue
        path = urlparse(url).path.strip('/')
        if not path:
            continue
        slugs.add(path.split('/', 1)[0])
    return sorted(slugs - ROOTS)


def make_rewriter(slugs: list[str], source_domain: str | None):
    asset_re = re.compile(r'(\.\./)+(wp-(?:content|includes))/')
    bare_asset_re = re.compile(rf'({ATTRS}=["\'])(wp-(?:content|includes)/)')
    srcset_re = re.compile(r'srcset=["\']([^"\']+)["\']')
    index_up_re = re.compile(rf'({ATTRS}=["\'])(\.\./)+index\.html')
    index_bare_re = re.compile(rf'({ATTRS}=["\'])index\.html(["\'#])')

    slug_passes = []
    for slug in slugs:
        s = re.escape(slug)
        slug_passes.append((re.compile(rf'(\.\./)+{s}/'), f'/{slug}/'))
        slug_passes.append((
            re.compile(rf'({ATTRS}=["\']){s}/'),
            rf'\1/{slug}/',
        ))

    abs_uploads_re = (
        re.compile(rf'https?://{re.escape(source_domain)}/wp-content/uploads/')
        if source_domain else None
    )

    def fix_srcset(match: re.Match[str]) -> str:
        out = []
        for entry in match.group(1).split(','):
            entry = entry.strip()
            if not entry:
                continue
            url, *rest = entry.split(None, 1)
            url = re.sub(r'^(?:\.\./)+(wp-(?:content|includes)/)', r'/\1', url)
            if url.startswith(('wp-content/', 'wp-includes/')):
                url = '/' + url
            out.append(' '.join([url, *rest]))
        return f'srcset="{", ".join(out)}"'

    def rewrite(html: str) -> str:
        html = asset_re.sub(r'/\2/', html)
        html = bare_asset_re.sub(r'\1/\2', html)
        html = srcset_re.sub(fix_srcset, html)
        for pattern, replacement in slug_passes:
            html = pattern.sub(replacement, html)
        html = index_up_re.sub(r'\1/', html)
        html = index_bare_re.sub(r'\1/\2', html)
        if abs_uploads_re is not None:
            html = abs_uploads_re.sub('/wp-content/uploads/', html)
        return html

    return rewrite


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output_dir', type=pathlib.Path)
    parser.add_argument('urls_file', type=pathlib.Path)
    parser.add_argument(
        '--source-domain',
        help='Strip this absolute origin from /wp-content/uploads/ URLs '
             '(og:image, lightbox hrefs, etc.). Bare hostname, no scheme.',
    )
    args = parser.parse_args()

    if not args.output_dir.is_dir():
        print(f'output_dir not found: {args.output_dir}', file=sys.stderr)
        return 1
    if not args.urls_file.is_file():
        print(f'urls_file not found: {args.urls_file}', file=sys.stderr)
        return 1

    slugs = page_slugs_from_urls(args.urls_file)
    rewrite = make_rewriter(slugs, args.source_domain)

    changed = 0
    for path in args.output_dir.rglob('*.html'):
        original = path.read_text(encoding='utf-8')
        new = rewrite(original)
        if new != original:
            path.write_text(new, encoding='utf-8')
            changed += 1
    print(f'rewrote {changed} files (slugs: {len(slugs)})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
