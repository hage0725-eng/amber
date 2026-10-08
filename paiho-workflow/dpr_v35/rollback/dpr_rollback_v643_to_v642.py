# -*- coding: utf-8 -*-
"""dpr_rollback_v643_to_v642.py — 由 dpr_suite.py v643 逐位元組重建 v642（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v643_to_v642.py dpr_suite.py dpr_suite_v642.py
做法：自 v643 _PACK 解出 tdt_link.py 套反向行差回 v2，以 suite 自帶 _z() 重新內嵌，套反向行差回 docstring／SUITE_VERSION，比對 SHA256。
再往前回 v641：接 dpr_rollback_v642_to_v641.py。
"""
import sys, json, hashlib, importlib.util
EXPECT_IN = '86bf5036ee2d21ff6add2b91f9bc88551535b052173f12ac129bebd6a6708e68'
EXPECT_OUT = 'f05b5879618758218aab151ee12c93283c8b0d3b80d59bba01f758ff995c73c9'
PATCH = json.loads('{"__suite__": [[1, 5, ["\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v642·1005 DPR 瘦身輪＋R-1004-3(b)＋R-1004-13）"]], [200, 201, ["SUITE_VERSION = 642   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）"]]], "tdt_link.py": [[0, 3, ["# FILE_VERSION = 2   # R-v555-1：降版閘門用·改本檔須同步遞增"]], [21, 22, ["FILE_VERSION = 2"]], [46, 49, []], [210, 211, ["               \'upd\': ((\'客改規格·R-1004-13 個案：%s→%s；\' % (_nv(order), case)) if case else \'\') + str(g(\'upd\') or \'\')[:60],"]]]}')

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v643（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s643', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    t = '\n'.join(apply(s._unz(s._PACK['tdt_link.py']).decode('utf-8').split('\n'), PATCH['tdt_link.py'])).encode('utf-8')
    lines = ['@@PACK:tdt_link.py@@' if l.startswith("    'tdt_link.py': '") else l for l in raw.decode('utf-8').split('\n')]
    lines = apply(lines, PATCH['__suite__'])
    out = '\n'.join(("    'tdt_link.py': '%s'," % s._z(t)) if l == '@@PACK:tdt_link.py@@' else l for l in lines).encode('utf-8')
    h = hashlib.sha256(out).hexdigest()
    open(dst, 'wb').write(out)
    print(h, '✅ v642 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
