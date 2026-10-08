# -*- coding: utf-8 -*-
"""dpr_rollback_v641_to_v640.py — 把 dpr_suite.py v641 逐位元組還原成 v640（R-1002-26 E6 備份閘·R-1003-34）
用法：python3 dpr_rollback_v641_to_v640.py dpr_suite.py dpr_suite_v640.py
做法：從 v641 的 _PACK 取出 build_dpr.py v608 → 還原為 v607；
      內嵌項（_PACK／_EMB）解壓後逐行反向補丁再以 xz preset 9e 重編碼；外殼（docstring、SUITE_VERSION 等）逐行反向補丁。
      成功時印出 SHA256 ffaf9b28… ✅（v640 原檔）。
"""
import sys, re, json, base64, lzma, hashlib
EXPECT_IN = 'd2ae9a160a8c100a21788baa39013ae41577a4450fccbfe81598ecd095979815'
EXPECT_OUT = 'ffaf9b280f191f84908aeb15071976036199075a60f11d3f698c46c66fd2e2b2'
PATCH = '/Td6WFoAAATm1rRGAgAhARwAAAAQz1jM4AJjAdNdAD2IiKckP31yd31aDtWVa/JWu9GCYt4iCBcWXwv/qyIkfUzeB/0nO167RlB+ros9qzjXFmrSJtbfSFGKaGHxQPUgQEFdhL4b6Q6BVtt5PYA7OT4ZMs/s5nQoyGsk02/ONLwYYy/XZDAO+VaG8CoZJ0JlBbYQMQ3FG1rRWHC/3P9Sb/GjUF1EDNdz3BwFUWSyIK1889W7Rd3yMXRGzzxLOIWCnTZ4PlVSvKEEkxlYo/S5hRDOMSNDoEzGqZBcvEX497PX5TbgYNqISHgB0wPx6b2Ln6yMlgH/1+skYBIvyQYcFe4ueOn5mjW0yCn/FbjHZW0cCM+D+SgTBxTcF0oZUb2Lv2/1IDH465YyDgHG+apKbvTLqqTagux0VIj9S6Bky8hXyzjmzq1O9Xc2os6nByg+q+SAxG4VA4CrxQP6+JcFALkIlmofVw3tvko0eS0KUD7dTnYPN1jC5syV5+ZKnLDCngdXrL2xc/YZlw7ipntPUMkjxqu2vPjHNId57sjs3Q9wiSwbLrXZq2njQZ1DlqN8pzvN7O/wsIv5mmviaepqC+4q5NivW5xigKdH8hm9RBtErEuagxDoaeR14kVnigDO/oRBFcZ7xnDAkr4AkDIkWJRAAADnw71n4YcZsgAB7wPkBAAA6XnzPbHEZ/sCAAAAAARZWg=='
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v641（SHA256 不符）'
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
