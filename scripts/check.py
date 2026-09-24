#!/usr/bin/env python3
"""Check generated content, static links, metadata, and document semantics."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
errors = []


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids = []
        self.links = []
        self.headings = []
        self.attrs = []
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.attrs.append((tag, a))
        if 'id' in a:
            self.ids.append(a['id'])
        if tag in {'a', 'link'} and 'href' in a:
            self.links.append(a['href'])
        if tag == 'img':
            self.links.append(a['src'])
            if not a.get('alt') or not a.get('width') or not a.get('height'):
                errors.append(f'{self.path}: image missing alt/dimensions')
        if tag in {'h1', 'h2', 'h3', 'h4'}:
            self.headings.append(int(tag[1]))
        if tag == 'script':
            errors.append(f'{self.path}: unexpected client-side script')


paths = [ROOT / 'index.html', ROOT / '404.html', ROOT / 'publications/index.html', *sorted((ROOT / 'work').glob('*/index.html'))]
docs = {p.resolve(): Document(p) for p in paths}
for path, d in docs.items():
    rel = path.relative_to(ROOT)
    if d.headings.count(1) != 1:
        errors.append(f'{rel}: expected exactly one h1')
    if any(b > a + 1 for a, b in zip(d.headings, d.headings[1:])):
        errors.append(f'{rel}: skipped heading level')
    if len(d.ids) != len(set(d.ids)):
        errors.append(f'{rel}: duplicate IDs')
    if not any(t == 'html' and a.get('lang') == 'ko' for t, a in d.attrs):
        errors.append(f'{rel}: Korean document language missing')
    for required in ['description', 'viewport']:
        if not any(t == 'meta' and a.get('name') == required and a.get('content') for t, a in d.attrs):
            errors.append(f'{rel}: {required} missing')
    if not any(t == 'main' and a.get('id') == 'main' for t, a in d.attrs):
        errors.append(f'{rel}: main skip target missing')
    for url in d.links:
        split = urlsplit(url)
        if split.scheme in {'http', 'https', 'mailto'}:
            continue
        if split.scheme or not url:
            errors.append(f'{rel}: unexpected link {url}')
            continue
        target = (ROOT / split.path.lstrip('/') if split.path.startswith('/') else path.parent / split.path).resolve() if split.path else path
        if target.is_dir():
            target /= 'index.html'
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f'{rel}: missing local target {url}')
        elif split.fragment and target in docs and unquote(split.fragment) not in docs[target].ids:
            errors.append(f'{rel}: missing anchor {url}')
    for tag, a in d.attrs:
        if tag == 'link' and a.get('rel') == 'canonical':
            expected = 'https://daeyeongcho.github.io/' + (str(rel).removesuffix('index.html'))
            if a.get('href') != expected:
                errors.append(f'{rel}: wrong canonical')

r = json.loads((ROOT / 'content/publications.json').read_text())
counts = Counter(p['type'] for p in r['papers'])
assert counts == {'journal': 3, 'conference': 4}, counts
assert len({p['id'] for p in r['papers']}) == 7
assert all('조대영' in p['authors'] for p in r['papers'])
assert r['papers'][0]['doi'] == '10.23019/kingpc.22.4.202608.002'
assert r['patent']['filed'] == '2025-01-10'
assert r['patent']['priority_date'] == '2024-10-29'
assert r['thesis']['year'] == 2026
home = (ROOT / 'index.html').read_text()
for old in ('top', 'about', 'stack', 'experience', 'research', 'education', 'contact'):
    assert old in docs[(ROOT / 'index.html').resolve()].ids, old
assert 'Sep 2026 – Present' in home and 'Incoming' not in home
assert not any('TODO' in p.read_text() or 'Lorem ipsum' in p.read_text() for p in paths)
assert (ROOT / 'assets/avatar.png').stat().st_size > 0
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(docs)} HTML pages; local links/anchors, heading hierarchy, metadata, legacy anchors, 7 papers + separate thesis, patent dates.')
