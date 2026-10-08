# -*- coding: utf-8 -*-
"""dpr_rollback_v638_to_v637.py — 把 dpr_suite.py v638 逐位元組還原成 v637（R-1002-26 E6 備份閘·R-1003-31）
用法：python3 dpr_rollback_v638_to_v637.py dpr_suite.py dpr_suite_v637.py
做法：從 v638 的 _PACK 取出 build_dpr.py v605 → 還原為 v604；_EMB 第 23 棒 dpr_regression_v0924_spec_round.py → 還原 A19 寫死 _r[4]／_r[6] 版；
      內嵌項（_PACK／_EMB）解壓後逐行反向補丁再以 xz preset 9e 重編碼；外殼（docstring、SUITE_VERSION 等）逐行反向補丁。
      成功時印出 SHA256 953983b2… ✅（v637 原檔）。
"""
import sys, re, json, base64, lzma, hashlib
EXPECT_IN = 'd3f33e5c93a8015c31eb51b71bf4ef083df1fb56316d10cc8ea9d046cfc85d7d'
EXPECT_OUT = '953983b2f33168f9fc12ebb643a0a9c1837c09cb17bb6de20ac3e41ebca40ef2'
PATCH = '/Td6WFoAAATm1rRGAgAhARwAAAAQz1jM4As6BRhdAD2IiKckP31yd31aDsXQzEnqCiF3quRzGVpcYPXbhSkkSNXnUe69irZ1rfLZzvpL8v+J04H6FB1AbUorly0JA93G/DuMIjvDqDyTOIXalelr8wohZHupZF3S6PIt5+y5ilvGJYR/Tp2FbjkH8JHNqKyMsq2FAB3OmyvkAq8p/ggmhuIdqb31zOhOCxMzfCB+7RAINDvcmcdY4wQyo0vOKNcLYG63rE/oMwsM4TKBOTaX+gKfdT0RbsHkEDkX6p4UTJ06kga5qdK3B9kC5bsaq4nQnSLH4UXXFjBBiPY0huuOc9aTijFMj2xAm9iw0zhqxIc3dSBJjwX598cvIrcJwiFJ2Irdl0ke2X93TiYcL57/2kGfjwIP4Fi9IlKpqhiEd0tPz45paxRrtszOPb43HriBF93rfqZlu/ylCuhH2nwxqmT9j9NbJGJU0L9/BFyCMIykqe64quhTnmwCiL4ME5lAdWf1dMOtamwy9GcflA/cfpPlzBotglYwFPichXdMaPDepPNktDhLZd8I40KNKTru2o0YfwIi2LaACuo2v1ltPf5KuNOvjpr3eO1V8D+mL8e4E3LvAuNE+Cmh/RBPIL2abrWf5u6UR1WVL23FC2brDAc/SG5nyv29XjENigQBB4pVntglrFPC9q2itaGtU7wDC3NRDjM2l69hg+L6Q86hx3mG8lCoWu/wxG0qmQTo7ISCDpmlCLmEXUMgphBQYSMtGoGXRazgKO3VYtBhr3NTC9xeQirV4uNtrR0diRSj5p1Tz0ruAM2/ceO41q3CP+s4dfczL9L3ttz4UJTeMQqp+0pv9Yw98ju8XCUwe+V5S/xJ3g/xGstRqWpqBSksrea/Cd63QnZePk7nZTbfeuTdh056826OeaLnR/3o+MsmDOS9ug1jzEtDkYzuL9RBCkxBZAfNMKcIP+FLlS0JASArshAZPdBACAJDW49/p7pqk1AIrxtCogI96dU6/f2NBzH1GpC75X6qlRT2iCHRfD05EomWlaFFoZ+9p5O8cS7gTPndJ62ntf57pPQtc00NSsEdnAsCYNln+Cu3TxkqayBZwzKnJwp6dKW0IuUnlJV1nxq4YFmWUsQjNRzbOnmTe2dmYO1Y5285zZu1WkQ77/frv6hFMbx5lhbnSsarAXWnvTROtmVHF0oZu088MV71YsB8YFeqtRMwZ5JRQQP9eUgaiE/PXHb6+2ee5zYP7nZaiaT7XxYBT5N6IKtHyOzrI6bjbel4pnkVi3a535xB/7UMzQZo2opyWITo3dlB5aCw9xHdmla18EY0o3c4SUTKL1pSdE6ShVpq9lLFoWHlknz/y/WScq58pQMf3VkJr5jRlhQK7IpO1HVkIieS47wuioBP2keQxSukH10TtK8iEsm2GhSHtGtJVksitAmpHHq0fngF6fcZOLx3YqdKdIYwOYpLPlge1OOrS+JWWZExw60dWEsJVrHhIOpk7UOFU8jbyBGSYkk2r2dNBx+GZ4ze5NgrriJ+cAwMrspCtU+QuTyEIgDQzxZ7me17vJIC7+F0vGaZdEJAxV0wUgOgEXazPIIIdccSP7yADpT2SoafdFY89V0NYUl1NmaBDjpFY/g1BWj4BqG1XOh9TBS39pYm0Id+68tLf9w3MnHvNJO5Daa9FYxD3Bvf/aDUvaa00ZbwFjyQHZMH0NjfsmYV4d3PF6eEnie35ZuZt7teTMYuq9RMDQ1ub01XFeulVtvipl0cCUJXR2RchmxkACUTX7GPY5PQAAG0CrsWAABGi2bascRn+wIAAAAABFla'
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v638（SHA256 不符）'
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
