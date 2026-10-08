# -*- coding: utf-8 -*-
"""dpr_rollback_v644_to_v643.py — 由 dpr_suite.py v644 逐位元組重建 v643（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v644_to_v643.py dpr_suite.py dpr_suite_v643.py
做法：自 v644 _PACK 解出 build_dpr.py 套反向行差回 v609，以 suite 自帶 _z() 重新內嵌，套反向行差回 docstring／SUITE_VERSION，比對 SHA256。
再往前：接 dpr_rollback_v643_to_v642.py → dpr_rollback_v642_to_v641.py。
"""
import sys, json, hashlib, importlib.util
EXPECT_IN = '61b685dd9bb00d995b1e9610c843c5c69fe154ef70daa31c6948eab2534a6208'
EXPECT_OUT = '86bf5036ee2d21ff6add2b91f9bc88551535b052173f12ac129bebd6a6708e68'
PATCH = json.loads('{"__suite__": [[1, 5, ["\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v643·1005 R-1005-19 BESTELLAR 同流水號比照）"]], [203, 204, ["SUITE_VERSION = 643   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）"]]], "build_dpr.py": [[1, 5, ["# FILE_VERSION = 609   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增"]], [3597, 3602, []], [3625, 3627, ["_ord = sorted(range(len(A1_ROWS)), key=lambda i: (A1_ROWS[i][1] or \'\', -A1_BY[i][0], A1_ROWS[i][3]))"]], [3739, 3741, []], [3885, 3887, ["HB3 = [\'狀態 / Trạng thái\', \'助理 / Trợ lý\', \'客戶代碼 / Mã KH\', \'客戶簡稱 / Tên tắt KH\', \'訂單號 / Mã đơn\',"]], [3911, 3919, []], [3932, 3933, ["                    *b3_prev(r[2], r[3], _od)])"]], [3953, 3956, ["                    *b3_prev(r[2], r[3], _od)])", "_b3k = lambda x: (0 if \'已過回復客戶日\' in x[0] else (1 if x[0].startswith(\'🧪\') else 2), -x[12], x[3])"]], [4011, 4014, ["write_table(wsB3, HB3, [x[:15] + x[16:18] for x in B3_ROWS] or [[\'本輪無完工足數未交單 / Không có\'] + [\'\'] * 16])"]]]}')
F = 'build_dpr.py'

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v644（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s644', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    t = '\n'.join(apply(s._unz(s._PACK[F]).decode('utf-8').split('\n'), PATCH[F])).encode('utf-8')
    lines = ['@@PACK:' + F + '@@' if l.startswith("    '%s': '" % F) else l for l in raw.decode('utf-8').split('\n')]
    lines = apply(lines, PATCH['__suite__'])
    out = '\n'.join(("    '%s': '%s'," % (F, s._z(t))) if l == '@@PACK:' + F + '@@' else l for l in lines).encode('utf-8')
    h = hashlib.sha256(out).hexdigest()
    open(dst, 'wb').write(out)
    print(h, '✅ v643 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
