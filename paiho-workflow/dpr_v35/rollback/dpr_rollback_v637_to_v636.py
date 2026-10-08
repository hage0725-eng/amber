# -*- coding: utf-8 -*-
"""dpr_rollback_v637_to_v636.py — 把 dpr_suite.py v637 逐位元組還原成 v636（R-1002-26 E6 備份閘·R-1003-30）
用法：python3 dpr_rollback_v637_to_v636.py dpr_suite.py dpr_suite_v636.py
做法：從 v637 的 _PACK 取出 build_dpr.py v604 → 依內嵌逐行反向補丁還原為 v603；刪 _PACK 之 tdt_link.py；
      再以反向補丁還原 docstring、SUITE_VERSION、PACK_GLOBS。成功時印出 SHA256 24ccc739… ✅（v636 原檔）。
"""
import sys, re, json, base64, lzma, hashlib
EXPECT_IN = '953983b2f33168f9fc12ebb643a0a9c1837c09cb17bb6de20ac3e41ebca40ef2'
EXPECT_OUT = '24ccc739db4e13ade1a797dfac91fae2027db8983f36b565a0b93a8210935e20'
PATCH = '/Td6WFoAAATm1rRGAgAhARwAAAAQz1jM4AKzAe5dAD2IigZT2x0zgCIwiywpC25OwlZz+TqcRU9DrmIt2UH1JKQ8qc1VCmY3eW87jZdVkV9Ix0Gr/4H9WZessUH5BgwQqP2Q+nF8I18MPT8B/uUYzP1DpTQHEf+qIA7llPuAu0d6CPOtdHPhCMwXQP+Q3PySCXbnRmDn9kLM4UQS6heFEhohytnqHOxlgtn5RaxXHfnvg2Yy0eV7tFAKWMjQANzCukniU+tXw6NFeyWeucSEnW+RnxVerEJQbwCgFt63W8Uv9ANXFTze6hNVAjhmrm61QT/c1K61AukXosS/qGjUOn7ef6cw++dWTRu97UoR8a6b/Nikx5vyw/PMpKjD9QfGcFt1kspihoONcNyKXUXPySMvgLYgfP5RcvQLXx4OwFsC89o7hcxWtsoJVdBhNYVrkSIT1EExjqirTI6YhtZUizvRaIAw1UOgqpp13An+xDC1lW1v52oYscWZW6ovRyWW5nyKZYMouFXTSffKdZ4S4v/7R3G+a7s6XQh/rHiFSRIz1pujTZ0v9mGmt7ZmSfT2hOSb80B2GGqgUX3bfq3Pgr3IkjbFdYtkggze6MrDopvp/SR0zYWBvkZRVn+VBv3Ycs41HwWwBb0VF/RGDR9i5t8inPatg+n3VQRh+D06xnrZnYBDrvTVRURDFwEAAAAANwkw5DEmoEwAAYoEtAUAAIVeJR2xxGf7AgAAAAAEWVo='
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v637（SHA256 不符）'
t = raw.decode('utf-8')
D = json.loads(lzma.decompress(base64.b64decode(PATCH)).decode('utf-8'))
def apply(s, ops):
    L = s.splitlines(True)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        L[i1:i2] = rep
    return ''.join(L)
z = lambda s: base64.b64encode(lzma.compress(s.encode('utf-8'), preset=9 | lzma.PRESET_EXTREME)).decode('ascii')
m = re.search(r"^_PACK = \{\n(.*?)^\}\n", t, re.S | re.M)
E = re.findall(r"    '([^']+)': '([A-Za-z0-9+/=]+)'", m.group(1))
out = []
for k, b in E:
    if k in D['pack']:
        if D['pack'][k] is None:
            continue
        b = z(apply(lzma.decompress(base64.b64decode(b)).decode('utf-8'), D['pack'][k]))
    out.append((k, b))
packtxt = '_PACK = {\n' + ',\n'.join("    '%s': '%s'" % kb for kb in out) + ',\n}\n'
shell = apply(t[:m.start()] + '@@PACK@@' + t[m.end():], D['shell'])
res = shell.replace('@@PACK@@', packtxt, 1).encode('utf-8'); h = hashlib.sha256(res).hexdigest()
open(dst, 'wb').write(res)
print('SHA256', h[:8] + '…', '✅' if h == EXPECT_OUT else '❌ 不符')
sys.exit(0 if h == EXPECT_OUT else 1)
