#!/usr/bin/env python3
"""Render a markdown draft to a browser-copyable HTML preview for Substack.

Usage: python3 scripts/render-draft.py drafts/<name>.md
Writes <name>-preview.html next to it. The H1 becomes the page <title>
only (Substack wants the title in its own field, not the body).
"""
import re, html, sys, os

src_path = sys.argv[1] if len(sys.argv) > 1 else 'drafts/blog0-three-home-lab-machines.md'
src = open(src_path).read()

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', t)
    return t

title, out, unhandled = os.path.basename(src_path), [], []
for block in re.split(r'\n\s*\n', src.strip()):
    lines = block.split('\n')
    first = lines[0]
    if first.startswith('# '):
        title = first[2:].strip()
    elif first.startswith('### '):
        out.append('<h3>%s</h3>' % inline(' '.join(l.strip() for l in lines)[4:]))
    elif first.startswith('## '):
        out.append('<h2>%s</h2>' % inline(' '.join(l.strip() for l in lines)[3:]))
    elif first.startswith('- '):
        items, cur = [], None
        for l in lines:
            if l.startswith('- '):
                if cur is not None: items.append(cur)
                cur = l[2:].strip()
            else:
                cur += ' ' + l.strip()
        items.append(cur)
        out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % inline(i) for i in items))
    elif first.startswith('>'):
        out.append('<blockquote><p>%s</p></blockquote>' % inline(' '.join(l.lstrip('> ').strip() for l in lines)))
    elif first.startswith(('|', '```', '1.')):
        unhandled.append(first[:60])
    else:
        out.append('<p>%s</p>' % inline(' '.join(l.strip() for l in lines)))

page = '''<!doctype html><html><head><meta charset="utf-8">
<title>%s</title>
<style>body{max-width:640px;margin:40px auto;font-family:Georgia,serif;font-size:17px;line-height:1.6;color:#222;padding:0 16px}h2{margin-top:1.6em}code{font-family:Menlo,monospace;font-size:.85em;background:#f4f4f4;padding:1px 4px;border-radius:3px}</style>
</head><body>
%s
</body></html>''' % (html.escape(title), '\n'.join(out))

dest = re.sub(r'\.md$', '', src_path) + '-preview.html'
open(dest, 'w').write(page)
print('title (for Substack title field):', title)
print('wrote:', dest)
if unhandled:
    print('WARNING - unhandled blocks (fix or paste these manually):')
    for u in unhandled: print('  ', u)
