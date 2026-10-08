# -*- coding: utf-8 -*-
"""dpr_rollback_v642_to_v641.py — 由 dpr_suite.py v642 逐位元組重建 v641（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v642_to_v641.py dpr_suite.py dpr_suite_v641.py
做法：① 自 v642 _PACK 解出 build_dpr.py／tdt_link.py／baoyan_weekly.py，套反向行差回 v608／v1／v3；
      ② 報延天數表 idx89c1 解碼回原 dict（鍵順序原樣）→ 同參數 json.dumps 逐位元組重建；
      ③ 以 suite 自帶 _z()（xz preset 9e）重新內嵌，套反向行差回 docstring／SUITE_VERSION；④ 比對 SHA256。
"""
import sys, json, hashlib, importlib.util
EXPECT_IN = 'f05b5879618758218aab151ee12c93283c8b0d3b80d59bba01f758ff995c73c9'
EXPECT_OUT = 'd2ae9a160a8c100a21788baa39013ae41577a4450fccbfe81598ecd095979815'
PATCH = json.loads('{"__suite__": [[1, 8, ["\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v641·1003 R-1003-34 未掛 DC 保留足視同完工）"]], [197, 198, ["SUITE_VERSION = 641   # R-v556-1（轉正·永久）：套件自版號（改 suite 必須同步改此常數）"]]], "build_dpr.py": [[1, 6, ["# FILE_VERSION = 608   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增"]], [189, 224, []], [976, 978, []], [992, 993, ["        _IDX89_EARLY.append((_json.load(open(_c[-1], encoding=\'utf-8\')).get(\'idx89\') or {}) if _c else {})"]], [1046, 1049, ["    bl_ok = dnz(r[39]) == \'✔\'"]], [2333, 2337, []], [3344, 3345, []], [3493, 3494, ["    if dnz(r[39]) == \'✔\' and _rsv89_state(r)[0]:   # R-1003-33：89 已入庫足或已到 97 才推定完工"]], [3511, 3512, ["                elif dnz(e[39]) == \'✔\':"]], [3643, 3644, []]], "tdt_link.py": [[0, 4, ["# FILE_VERSION = 1   # R-v555-1：降版閘門用·改本檔須同步遞增"]], [19, 20, ["FILE_VERSION = 1"]], [40, 55, []], [176, 178, ["        for c in self.cands(order):"]], [184, 187, []], [204, 206, ["               \'text\': txt, \'ship\': _asd(g(\'ship\')), \'done\': g(\'done\'), \'upd\': str(g(\'upd\') or \'\')[:60],"]]], "baoyan_weekly.py": [[1, 3, ["# FILE_VERSION = 3"]], [26, 54, []], [315, 316, ["               not_adopted=[list(x) for x in LOWER if x[1] == \'L1\'], idx89=idx89, idx89_window=dict(start=str(dates[0]), end=str(dates[-1]), snapshots=len(dates), dup_skipped=len(DUP_SKIPPED)),"]]]}')
PN = ['build_dpr.py', 'tdt_link.py', 'baoyan_weekly.py', '報延天數表_v20261003.json']

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v642（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s642', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    files = {}
    for n in PN[:3]:
        files[n] = '\n'.join(apply(s._unz(s._PACK[n]).decode('utf-8').split('\n'), PATCH[n])).encode('utf-8')
    j = json.loads(s._unz(s._PACK[PN[3]]))
    x = j['idx89']; D, P = x['D'], x['P']
    vv = [[D[a], P[b], bool(f >> 1), bool(f & 1), t] for a, b, f, t in x['V']]
    j['idx89'] = {'%s|%s' % (a, b): list(vv[i]) for a, b, i in zip(x['o'], x['s'], x['i'])}
    files[PN[3]] = json.dumps(j, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    lines = []
    for l in raw.decode('utf-8').split('\n'):
        hit = next((n for n in PN if l.startswith("    '%s': '" % n)), None)
        lines.append('@@PACK:%s@@' % hit if hit else l)
    lines = apply(lines, PATCH['__suite__'])
    out = '\n'.join(("    '%s': '%s'," % (l[7:-2], s._z(files[l[7:-2]]))) if l.startswith('@@PACK:') else l for l in lines).encode('utf-8')
    h = hashlib.sha256(out).hexdigest()
    open(dst, 'wb').write(out)
    print(h, '✅ v641 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
