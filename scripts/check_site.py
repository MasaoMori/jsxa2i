"""Check generated HTML: links, assets, language switches and draft notices."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys
root = Path(sys.argv[1] if len(sys.argv) > 1 else 'public').resolve()
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.ids=set(); self.h1=0; self.notice=False; self.switches={}; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
        if 'id' in a: self.ids.add(a['id'])
        if tag=='h1': self.h1+=1
        if 'concept-notice' in a.get('class','').split(): self.notice=True
        if tag=='a' and 'hreflang' in a: self.switches[a['hreflang']]=a.get('href','')
files={p:Page(p.read_text()) for p in root.rglob('*.html')}
assert files, 'No HTML generated'
first=next(iter(files.values()))
css=next(x for x in first.links if x.endswith('/assets/css/style.css'))
base=(sys.argv[2] if len(sys.argv)>2 else urlsplit(css).path.removesuffix('/assets/css/style.css')).rstrip('/')
errors=[]
for file,page in files.items():
    text=file.read_text()
    if '{{' in text or '{%' in text: errors.append(f'Unrendered template: {file}')
    if not page.notice or page.h1!=1: errors.append(f'Notice or H1 invalid: {file}')
    if set(page.switches)!={'en','ja'}: errors.append(f'Language switches missing: {file}')
    for link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc: continue
        path=unquote(u.path)
        if path.startswith('/'):
            if base and not (path==base or path.startswith(base+'/')):
                errors.append(f'Missing subpath: {file}: {link}'); continue
            target=root/path.removeprefix(base).lstrip('/')
        else: target=file.parent/path if path else file
        if target.is_dir(): target=target/'index.html'
        target=target.resolve()
        if not target.is_file(): errors.append(f'Broken link: {file}: {link}')
        elif u.fragment and target in files and unquote(u.fragment) not in files[target].ids:
            errors.append(f'Broken fragment: {file}: {link}')
for lang in ('en','ja'):
    for key in ('','mission','principles','applied-informatics','activities','organizations','resources','contact'):
        p=root/lang/key/'index.html'
        if p not in files: errors.append(f'Missing page: {p}')
        elif key:
            other='ja' if lang=='en' else 'en'
            expected=f'{base}/{other}/{key}/'
            if files[p].switches.get(other)!=expected: errors.append(f'Incorrect translation target: {p}')
for p in (root/'index.html', root/'en/index.html'):
    if p not in files or 'http-equiv="refresh"' in p.read_text(): errors.append(f'English home is not direct HTML: {p}')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(files)} HTML pages; internal links, fragments, assets, language switches, H1 and draft notices (baseurl={base!r})')
