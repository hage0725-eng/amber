# -*- coding: utf-8 -*-
"""dpr_rollback_v647_to_v646.py — 由 dpr_suite.py v647 逐位元組重建 v646（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v647_to_v646.py dpr_suite.py dpr_suite_v646.py
做法：自 v647 _PACK 解出 build_dpr.py 套反向行差回 v612，以 suite 自帶 _z() 重新內嵌，套反向行差回 docstring／SUITE_VERSION，比對 SHA256。
再往前：接 dpr_rollback_v646_to_v645.py → … → v642_to_v641。
"""
import sys, json, hashlib, importlib.util
EXPECT_IN = '89d16a32b2bf1aad5e29bd77bcd61f5ca8db7971c4c09581f501d74cdb4db9c2'
EXPECT_OUT = '388ee2363d7d7d0d9094af77b59a02e9cc3a6a4033130f5b18665bb95e13f362'
PATCH = json.loads("{\"build_dpr.py\": [[1, 10, [\"# FILE_VERSION = 612   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\"]], [1040, 1044, []], [1093, 1094, [\"                 or (over_kh is not None) or test == 'F')\"]], [1096, 1097, [\"                or o19_status == 'not_delay' or test == 'Q' or yarn or bl_ok)\"]], [1117, 1122, [\"            if over_kh is not None:\"]], [1132, 1134, []], [1175, 1176, [\"        risk = HIGH if (over_kh is not None or yarn or test == 'F') else MEDH\"]], [1197, 1201, []], [1230, 1231, [\"                'ntns': ntns_of(r[11]), 'sc': sc, 'nv': nv_val, 'tl': tl_val, 'b1': b1_days, 'b2': b2_days, 'okh': over_kh,\"]], [3623, 3624, []], [3637, 3638, [\"        tier = _tier(okh)\"]], [3678, 3686, []], [3834, 3836, []], [4006, 4007, [\"        (B3_EX.append((x, td_)) if (td_['status'] == 'OK' and td_['date'] > TODAY) else _b3keep.append(x))\"]], [4009, 4010, [\"    assert not any((lambda t: t['status'] == 'OK' and t['date'] > TODAY)(_TLK.link(dnz(x[2]), dnz(x[4]), dnz(x[7]))) for x in B3_ROWS), \\\\\"]], [4035, 4036, []]], \"__suite__\": [[1, 6, [\"\\\"\\\"\\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v646·1005 R-1005-22 TDT 去「 CT」尾碼＋原單防呆）\"]], [213, 214, [\"SUITE_VERSION = 646   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）\"]]]}")
FILES = ['build_dpr.py']

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v647（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s647', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
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
    print(h, '✅ v646 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
