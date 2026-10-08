# -*- coding: utf-8 -*-
"""dpr_rollback_v646_to_v645.py — 由 dpr_suite.py v646 逐位元組重建 v645（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v646_to_v645.py dpr_suite.py dpr_suite_v645.py
做法：自 v646 _PACK 解出 build_dpr.py / tdt_link.py 套反向行差回 v645 版，以 suite 自帶 _z() 重新內嵌，套反向行差回 docstring／SUITE_VERSION，比對 SHA256。
再往前：接 dpr_rollback_v645_to_v644.py → v644_to_v643 → v643_to_v642 → v642_to_v641。
"""
import sys, json, hashlib, importlib.util
EXPECT_IN = '388ee2363d7d7d0d9094af77b59a02e9cc3a6a4033130f5b18665bb95e13f362'
EXPECT_OUT = '2dd3432166181b13d3107774b89c402ab1325ff107401901c10e601ad0144685'
PATCH = json.loads('{"build_dpr.py": [[1, 4, ["# FILE_VERSION = 611   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增"]], [3651, 3652, ["        A1_TDT = [_TLK.link(dnz(x[2]), dnz(x[4]), dnz(x[7])) for x in A1_ROWS]"]]], "tdt_link.py": [[0, 4, ["# FILE_VERSION = 4   # R-v555-1：降版閘門用·改本檔須同步遞增"]], [26, 27, ["FILE_VERSION = 4"]], [80, 81, []], [183, 186, ["    def link(self, code, order, pn=None):", "        \\"\\"\\"回傳 dict：status ∈ {\'無TDT對應\',\'未找到\',\'TDT無日期\',\'OK\'}，OK 時帶 date/src/file/row/ship/multi。\\"\\"\\""]], [190, 193, []], [214, 221, []], [229, 230, ["               \'upd\': ((\'%s 個案：%s→%s；\' % ((\'客改規格·R-1004-13\' if \'-3MM\' in _nv(order) else \'客改規格·R-1005-19\' if \'MM\' in _nv(order) else \'同流水號比照·R-1005-19\'), _nv(order), case)) if case else \'\') + str(g(\'upd\') or \'\')[:60],"]]], "__suite__": [[1, 5, ["\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v645·1005 R-1005-21 T1 帶 TDT·SGV(ON)）"]], [209, 210, ["SUITE_VERSION = 645   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）"]]]}')
FILES = ['build_dpr.py', 'tdt_link.py']

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v646（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s646', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
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
    print(h, '✅ v645 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
