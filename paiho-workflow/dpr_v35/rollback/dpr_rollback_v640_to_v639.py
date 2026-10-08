# -*- coding: utf-8 -*-
"""dpr_rollback_v640_to_v639.py — 把 dpr_suite.py v640 逐位元組還原成 v639（R-1002-26 E6 備份閘·R-1003-33）
用法：python3 dpr_rollback_v640_to_v639.py dpr_suite.py dpr_suite_v639.py
做法：從 v640 的 _PACK 取出 build_dpr.py v607 → 還原為 v606；_EMB 第 23 棒 → 還原 A19 舊字串、刪 A19g；
      內嵌項（_PACK／_EMB）解壓後逐行反向補丁再以 xz preset 9e 重編碼；外殼（docstring、SUITE_VERSION 等）逐行反向補丁。
      成功時印出 SHA256 86b753a8… ✅（v639 原檔）。
"""
import sys, re, json, base64, lzma, hashlib
EXPECT_IN = 'ffaf9b280f191f84908aeb15071976036199075a60f11d3f698c46c66fd2e2b2'
EXPECT_OUT = '86b753a89827d4b69be9026c0d5f6f76c24db62b377e7358b41043e1c0d0c48b'
PATCH = '/Td6WFoAAATm1rRGAgAhARwAAAAQz1jM4ARfAyJdAD2IiKckP31yd31aDsXQzEnqDQsO2JdM1NPnU35qaDC3dkKZ/3ufIPD9PHpPEMTeg6ab9m+9j/c/kZ+gzFeAtceaxroD74ezdhCisEZjNdgCiMlvieXoIVFSBgAN76+RfP/nRwAkng86P9moZ9q8nInYoPcPudMLFfFXyqZ6fxrLEFq2ujxpEPn3zjT2fH2XMgy+tW1Hhsey/eQdNXfG6TJB5zJQUvDKJlDoNm9jucnt5zoGh+8ib9lIjpEjtvqGBjeY6zWHKsvwnhKpeYp64Hwoshj6y6pCiyQl2Bk9FMCY0K1F5zkjVBnQaEScJrfK1n45aHGpYlYqOauHPpU2x5Yt9ewJh+5sKFh/dIf5lQFKDerL9qP7pCU9w8UPobmXZMukYe17mGHZW0BygAhATiojUXBEwBdAlQS86nTLDwYij268WEA2Y+FdhilieEZU3j06WWK8hl4giMHDYcstjD2xh0XtieWbGi7MoyM86qghUjDJfHSQQkbjmwq96vlwCpVWIfh8Kx32E7JgcBuOz6lDOY8WZtUG6mmELjbruM96/u94YxmWsLllYxvT9ZFQgokIw0akoVtlKbqddKWMjkn/dGTH8w+ZbD1mwl3k/Fb0P98nrhmTN7i+DUFD4vaO4Gm6Nos4XJkPMOwE5a8n854g5280BE4Jaqo80qIUurHxr4fMBPLzgiByDAP5o6niMInrN6p1HwTm27cj6KrOVXQdNC/iJ8QwGN04Zln0obBW8c/aJxYRDlGc7Kqr9HnGM0UkaZyHOdtogXpxTBvcSpNdTO2EX+qGWqIjZXdb2ldC80sDhhkn4KpNZmVAFzHvO6JuEH8JwkgjNhEVly8g8DsFcjBgVRE61Npd63i+AGNa/Z4lVegIwdPEpJXGP8ox8MTp0FsAgJZQXF4DRiBxciXEsFFJuCQ6iowPH7TfRYvF2PuXYJG+nutLtFWdA0V/eTIfY9iIsNCV8fqRbZCC21lt3dLEFuA3oM2UPlXG4+YH5eaYjrCekgUt3Gnz6K15SwpsokcUO83PlDpSGYSL9avWE2Wonx7/ksXaZBg6835FM4gAAACn9oWWivkApQABvgbgCAAA+EO5tLHEZ/sCAAAAAARZWg=='
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v640（SHA256 不符）'
t = raw.decode('utf-8')
D = json.loads(lzma.decompress(base64.b64decode(PATCH)).decode('utf-8'))
def apply(s, ops):
    L = s.splitlines(True)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        L[i1:i2] = rep
    return ''.join(L)
E = []
def f(m):
    E.append(m.group(3)); return m.group(1) + '@@%d@@' % (len(E) - 1) + m.group(4)
shell = re.sub(r"^(    '([^']+)': ')([A-Za-z0-9+/=]{64,})(')", f, t, flags=re.M)
for i, ops in D['ent'].items():
    if ops is not None:
        E[int(i)] = base64.b64encode(lzma.compress(apply(lzma.decompress(base64.b64decode(E[int(i)])).decode('utf-8'), ops).encode('utf-8'),
                                                   preset=9 | lzma.PRESET_EXTREME)).decode('ascii')
shell = apply(shell, D['shell'])
res = re.sub(r'@@(\d+)@@', lambda m: E[int(m.group(1))], shell).encode('utf-8'); h = hashlib.sha256(res).hexdigest()
open(dst, 'wb').write(res)
print('SHA256', h[:8] + '…', '✅' if h == EXPECT_OUT else '❌ 不符')
sys.exit(0 if h == EXPECT_OUT else 1)
