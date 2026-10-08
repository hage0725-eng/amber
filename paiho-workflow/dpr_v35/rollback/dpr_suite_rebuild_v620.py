# -*- coding: utf-8 -*-
"""dpr_suite_rebuild_v620.py — DPR 瘦身輪（2026-10-01·Amber 林彥博「DPR 瘦身輪=>執行」）回滾工具
用途：由 v621（瘦身版）＋版本沿革檔，逐位元組重建 v620 原檔（SHA256 575822d3…）。
用法：python3 dpr_suite_rebuild_v620.py dpr_suite.py dpr_suite_版本沿革_v575-v618_移出.md  → 產出 dpr_suite_v620.py
"""
import sys, re, base64, lzma, hashlib
WANT = '575822d3e0a2ac9d435800341247e6e27327029eeb495162a2406ab3a64a8776'
src, hist = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
h = open(hist, encoding='utf-8').read()
moved = h.split('```text\n', 1)[1].rsplit('\n```', 1)[0]
i = s.index('"""'); j = s.index('"""', i + 3)
L = s[i:j].split('\n')
k_ptr = next(n for n, l in enumerate(L) if l.startswith('（v618–v575 共 30 則版本沿革'))
k620 = next(n for n, l in enumerate(L) if l.startswith('v620（'))
head = L[0].replace('（v621·1001 DPR 瘦身輪）', '（v600·0916 H1 裁示輪）')
doc = '\n'.join([head] + L[k620:k_ptr] + moved.split('\n') + L[k_ptr + 1:])
s = s[:i] + doc + s[j:]
out = []; in_emb = False
for ln in s.split('\n'):
    if ln.startswith('_EMB = {'): in_emb = True
    elif in_emb and ln.startswith('}'): in_emb = False
    m = in_emb and re.match(r"^(\s*)'([^']+)': '([A-Za-z0-9+/=]+)'(,?)$", ln)
    if m:
        raw = base64.b64decode(m.group(3))
        if raw[:6] == b'\xfd7zXZ\x00':
            ln = "%s'%s': '%s'%s" % (m.group(1), m.group(2), base64.b64encode(lzma.decompress(raw)).decode(), m.group(4))
    out.append(ln)
s = '\n'.join(out)
s = re.sub(r"def _src\(name\):\n    # v621.*?\n    raw = .*?\n    return .*?\n",
           "def _src(name):\n    return _b64.b64decode(_EMB[name]).decode('utf-8')\n", s, count=1, flags=re.S)
s = s.replace('SUITE_VERSION = 621', 'SUITE_VERSION = 620', 1)
open('dpr_suite_v620.py', 'w', encoding='utf-8').write(s)
got = hashlib.sha256(s.encode('utf-8')).hexdigest()
print('SHA256', got, '✅ 與 v620 原檔一致' if got == WANT else '❌ 不一致')
sys.exit(0 if got == WANT else 1)
