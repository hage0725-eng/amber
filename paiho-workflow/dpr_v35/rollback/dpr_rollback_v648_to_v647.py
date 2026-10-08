# -*- coding: utf-8 -*-
"""dpr_rollback_v648_to_v647.py — 由 dpr_suite.py v648 逐位元組重建 v647（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v648_to_v647.py dpr_suite.py dpr_suite_v647.py
做法：自 v648 _PACK 解出字典 v98／NT/NS v514 → 移除 R-1006-17 攝取項重編回 v97／v513 → 以 suite 自帶 _z() 重新內嵌；
      還原 docstring／SUITE_VERSION；比對 SHA256。再往前：接 dpr_rollback_v647_to_v646.py。
"""
import sys, json, hashlib, importlib.util, os
EXPECT_IN = '0402add88535494d32edc9aaf12ad3f85a2dec3b2a42adc9b373881b9358b7e6'
EXPECT_OUT = '89d16a32b2bf1aad5e29bd77bcd61f5ca8db7971c4c09581f501d74cdb4db9c2'
DOC = json.loads('[["\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v648·1006 R-1006-17 1005 回傳攝取：字典 v98／NT/NS v514）\\nv648（2026-10-06·**R-1006-17**·Amber 林彥博「回填更新」＋回傳 T組進度完整分析_1005_v644.xlsx〔SHA256-8 f98260b1〕）：\\n  · 回填原因處置字典 v97→**v98**：b3_replies +189（未到客戶交期 129／異常未交 60）；orders 2,316→2,317（4 表新 1 單）；6b 既有 11 單只加 r1006_17_evidence，6b 新見 3 單只存證於 rule_R_1006_17（不建 orders·6b 照列）；\\n    rule_R_1006_17（含 ingest_gate6：21 頁·系統欄 21,160 格 0 差異）。phrase_classifier_v35 一行未動。\\n  · ntns_dict v513→**v514**：+5（81Q5607OA／81Q5607VA／81QF3806V＝NT；81RCKQ2VH／81RCQ339V＝NS）。\\n  · builder v613、23 棒、快照 v579、overrides v1.11、tdt_link v5、報延天數表 一行未動；只換 _PACK 兩檔。SUITE_VERSION 647 → 648（R-v556-1）。\\n", "\\"\\"\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v647·1006 R-1006-15 DGT 測試單／R-1006-16 今天到期完工判定／R-1006-1 🧪留 B3）\\n"], ["SUITE_VERSION = 648   #", "SUITE_VERSION = 647   #"]]')

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v648（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s648', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    sys.path.insert(0, os.path.dirname(os.path.abspath(dst)) or '.')
    import types
    cod = types.ModuleType('dict_v14_codec'); exec(s._unz(s._PACK['dict_v14_codec.py']).decode('utf-8'), cod.__dict__)
    D = cod.load_any_bytes(s._unz(s._PACK['回填原因處置字典_v98_columnar.json'])) if hasattr(cod, 'load_any_bytes') else None
    if D is None:
        import tempfile
        t = tempfile.NamedTemporaryFile(suffix='_columnar.json', delete=False); t.write(s._unz(s._PACK['回填原因處置字典_v98_columnar.json'])); t.close()
        D = cod.load_any(t.name)
    R = D.pop('rule_R_1006_17'); D.pop('note_v98')
    for k in [k for k, v in D['b3_replies']['items'].items() if v.get('ingest') == 'R-1006-17']:
        del D['b3_replies']['items'][k]
    for k in R['orders_new']:
        del D['orders'][k]
    for v in D['orders'].values():
        v.pop('r1006_17_evidence', None)
    D['count'] = len(D['orders']); D['version'] = 'v97'; D['updated'] = '2026-10-03'
    dct = json.dumps(cod.encode(D), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    N = json.loads(s._unz(s._PACK['ntns_dict_v514.json']).decode('utf-8'))
    for k in N['note_v514']['added']:
        del N['keys'][k]
    N.pop('note_v514'); N['rulings'].pop()
    from collections import Counter
    N['counts'] = dict(Counter(N['keys'].values())); N['version'] = 'v513'; N['updated'] = '2026-10-02'; N['date'] = '2026-10-02'
    ntn = json.dumps(N, ensure_ascii=False, indent=1).encode('utf-8')
    rep = {"    '回填原因處置字典_v98_columnar.json': '": "    '回填原因處置字典_v97_columnar.json': '%s'," % s._z(dct),
           "    'ntns_dict_v514.json': '": "    'ntns_dict_v513.json': '%s'," % s._z(ntn)}
    lines = []
    for l in raw.decode('utf-8').split('\n'):
        hit = [k for k in rep if l.startswith(k)]
        lines.append(rep[hit[0]] if hit else l)
    txt = '\n'.join(lines)
    for a, b in DOC:
        assert txt.count(a) == 1, a[:40]
        txt = txt.replace(a, b)
    out = txt.encode('utf-8')
    h = hashlib.sha256(out).hexdigest()
    open(dst, 'wb').write(out)
    print(h, '✅ v647 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
