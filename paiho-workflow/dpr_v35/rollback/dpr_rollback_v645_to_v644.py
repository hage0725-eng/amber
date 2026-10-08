# -*- coding: utf-8 -*-
"""dpr_rollback_v645_to_v644.py — 由 dpr_suite.py v645 逐位元組重建 v644（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v645_to_v644.py dpr_suite.py dpr_suite_v644.py
做法：自 v645 _PACK 解出 build_dpr.py / tdt_link.py 套反向行差回 v644 版，以 suite 自帶 _z() 重新內嵌，套反向行差回 docstring／SUITE_VERSION，比對 SHA256。
再往前：接 dpr_rollback_v644_to_v643.py → v643_to_v642 → v642_to_v641。
"""
import sys, json, hashlib, importlib.util
EXPECT_IN = '2dd3432166181b13d3107774b89c402ab1325ff107401901c10e601ad0144685'
EXPECT_OUT = '61b685dd9bb00d995b1e9610c843c5c69fe154ef70daa31c6948eab2534a6208'
PATCH = json.loads('{"build_dpr.py": [[1, 4, ["# FILE_VERSION = 610   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增"]], [3636, 3637, ["if GROUP != \'T組\':", "    TDT_MSG = \'T1組不帶 TDT\'", "elif _TL is None or not _TL.root():"]]], "tdt_link.py": [[0, 3, ["# FILE_VERSION = 3   # R-v555-1：降版閘門用·改本檔須同步遞增"]], [23, 24, ["FILE_VERSION = 3"]], [43, 45, []]], "__suite__": [[1, 5, ["\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v644·1005 R-1005-20 A1／B3 預設排序＋B3 業務欄）"]], [206, 207, ["SUITE_VERSION = 644   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）"]]]}')
FILES = ['build_dpr.py', 'tdt_link.py']

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v645（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s645', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    packed = {F: s._z('\n'.join(apply(s._unz(s._PACK[F]).decode('utf-8').split('\n'), PATCH[F])).encode('utf-8')) for F in FILES}
    lines = []
    for l in raw.decode('utf-8').split('\n'):
        hit = [F for F in FILES if l.startswith("    '%s': '" % F)]
        lines.append('@@PACK:' + hit[0] + '@@' if hit else l)
    lines = apply(lines, PATCH['__suite__'])
    rev = {'@@PACK:' + F + '@@': "    '%s': '%s'," % (F, packed[F]) for F in FILES}
    out = '\n'.join(rev.get(l, l) for l in lines).encode('utf-8')
    h = hashlib.sha256(out).hexdigest()
    open(dst, 'wb').write(out)
    print(h, '✅ v644 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
