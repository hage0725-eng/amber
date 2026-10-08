# -*- coding: utf-8 -*-
"""dpr_rollback_v639_to_v638.py — 把 dpr_suite.py v639 逐位元組還原成 v638（R-1002-26 E6 備份閘·R-1003-32）
用法：python3 dpr_rollback_v639_to_v638.py dpr_suite.py dpr_suite_v638.py
做法：從 v639 的 _PACK 取出 build_dpr.py v606 → 還原為 v605；
      內嵌項（_PACK／_EMB）解壓後逐行反向補丁再以 xz preset 9e 重編碼；外殼（docstring、SUITE_VERSION 等）逐行反向補丁。
      成功時印出 SHA256 d3f33e5c… ✅（v638 原檔）。
"""
import sys, re, json, base64, lzma, hashlib
EXPECT_IN = '86b753a89827d4b69be9026c0d5f6f76c24db62b377e7358b41043e1c0d0c48b'
EXPECT_OUT = 'd3f33e5c93a8015c31eb51b71bf4ef083df1fb56316d10cc8ea9d046cfc85d7d'
PATCH = '/Td6WFoAAATm1rRGAgAhARwAAAAQz1jM4AQIArVdAD2IiKckP31yd31aDtWVa/JWu9GCZH+iKjEHDPagZCYqMrI5//dXC1k0So+8GxLJkTRxGkcRURTqpJaI0O7bf3JSCH08NNDVCnN5r3h591YWY/kHhwwb243xPvtB43FW77cIC9LwI2tliAR5iUqKTHSNIo0TMQsPqNChxKkXFWKdDb/GboTGBOzCt/x7zwIhtrPBf3Mz1qDMsIh6uPs8WIZeJwolEZih1Y//udcJjOzWLJmjuvJ9PFWUjMR8myICNhsD/4nFTlO15QnMQiK6kYYoMbW3m97/AxlyEtsWCcsV/cxOAW/CK30baVCAC90/HfXzblmCgupyTQL5gCQdfmMqkwIlqOUeCZsprzXtjrpSFIzdLuU06QCZBCks106siv434CeCuQJkhDMyw50Lo9P20vtbTN+INr95kV0g0caCOd93SPtuf7W4wU69o4R07tZJRooQjOjWYAzNBtifiT+99vDnBqNcA37ILypzDozmAv+sP8vN9aSkF8lXYDXpFVo2qcZo2i1cZy/c+3KEIHovsUA0m/K+1SzzWj41SsZp3dodhBLxRVI3zpxhGZz9cRKz/4SH44sc2rKy2MYtNjtkdU1kyhR4e4CwUauNmXJUvKsVQIX40D0NiQFZNB1Y0z9n3rUoZFkjUU64UMG3zdcMb9dNabjB6CGSHPajutjQB7LLu1CFs9Srbi2hPJjqyfmsQ6LMJ6BkNskTiOqF+fbkJg2l/xMj6LcvnaSxXa8Ng3oPqvBEJ2jzYK6DbZfA5C4GqWtnuLxhygqzY93/jqIMRrCQC25BXOZpO7YTKFPUnJvRbrjbPJuIaFfFfuTgndXnYswjnF43jECWLU5VQuZE2WESO07fypu7h1qYixFCYVu37fdf8MMU8xqIF50hAM2MO/5IXpP41Qj0XS9hH4VcdJpKAAAAAABpQH5nw7zH/wAB0QWJCAAALjyVTLHEZ/sCAAAAAARZWg=='
src, dst = sys.argv[1], sys.argv[2]
raw = open(src, 'rb').read()
assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v639（SHA256 不符）'
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
