# -*- coding: utf-8 -*-
"""dpr_rollback_v649_to_v648.py — 由 dpr_suite.py v649 逐位元組重建 v648（R-1002-26 上線閘·回滾程式）
用法：python3 dpr_rollback_v649_to_v648.py dpr_suite.py dpr_suite_v648.py
做法：builder v614 套反向行差回 v613；字典 v99 移除 R-1006-18～21 變更重編回 v98；以 suite 自帶 _z() 重新內嵌；還原 docstring／SUITE_VERSION；比對 SHA256。
再往前：接 dpr_rollback_v648_to_v647.py。
"""
import sys, json, hashlib, importlib.util, tempfile, types
EXPECT_IN = '24361c94c2ce26d5026897c361764d4a1d250ceb3e3f9655c9b4759c295547be'
EXPECT_OUT = '0402add88535494d32edc9aaf12ad3f85a2dec3b2a42adc9b373881b9358b7e6'
PATCH = json.loads("{\"build_dpr.py\": [[1, 7, [\"# FILE_VERSION = 613   # R-v555-1（Amber 0730「轉正」）：降版閘門用·改本檔須同步遞增\"]], [1023, 1025, []], [1050, 1052, [\"    is_dgt = (not is89) and ('DGT' in order)   # R-1006-15：所有 DGT 測試單\"]], [1140, 1143, [\"            if is_dgt:   # R-1006-15\"]], [1207, 1208, [\"        if '🧪DGT測試單' in rtxt:   # R-1006-15\"]], [1402, 1404, [\"_RX_PERIOD_TAIL = re.compile(r'^(?:[\\\\s\\\\.\\\\,\\\\-:;/()]+(?:NB|FORECAST|FOR|REFERENCE|REF|FC|BP\\\\d*|S{1,2}\\\\d{2}|F{1,2}\\\\d{2}|FW\\\\d{2}'\", \"                             r'|AW\\\\d{2}|T\\\\d{1,2}|\\\\d{1,4}(?:[\\\\./-]\\\\d{1,4})*))+[\\\\s\\\\.\\\\,\\\\-:;/()]*$')\"]], [3691, 3693, [\"assert all((x[0] == DGT_TIER) == ('DGT' in x[4] and not str(x[0]).startswith('⓪')) for x in A1_ROWS), 'R-1006-15 違例：A1 DGT 列級別錯置'\", \"assert all(('🧪DGT測試單' in a['reasons']) == (a['dgt'] and a['level'] != 'OK') for a in ANA if not a['is89']), 'R-1006-15 違例：DGT 標註不符'\"]]]}")
DOC = json.loads("[[\"\\\"\\\"\\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v649·1006 R-1006-18～21 抓比後綴／測試取結果單／XLBT／6b 入觀察）\\nv649（2026-10-06·**R-1006-18～21**·Amber 林彥博「T10-ok」「11-ok」「12-核對錯庫存導致重複備料，要求寫XLBT」「6b-入觀察名單」）：\\n  · build_dpr.py v613→**v614**：制度③後綴擴及抓比比例 *NN%（R-1006-18）；TEST_ONLY_CASES 個案白名單 010671 ANNORA VQNK26061528-1TN 比照 DGT（R-1006-19）。\\n  · 回填原因處置字典 v98→**v99**：6b 新見 3 張 89 建檔入觀察名單（R-1006-21·orders 2,317→2,320）；8926077572／8926070495 改「待開 XLBT」並設主管提問 directive（R-1006-20）；\\n    rule_R_0917_33 加 R-1006-18 修訂註記。23 棒、快照 v579、NT/NS v514、overrides v1.11、tdt_link v5、報延天數表 一行未動。SUITE_VERSION 648 → 649（R-v556-1）。\\n\", \"\\\"\\\"\\\"dpr_suite.py — DPR 迴歸/迴路單檔套件（v648·1006 R-1006-17 1005 回傳攝取：字典 v98／NT/NS v514）\\n\"], [\"SUITE_VERSION = 649   #\", \"SUITE_VERSION = 648   #\"]]")

def apply(lines, ops):
    out = list(lines)
    for i1, i2, rep in sorted(ops, key=lambda o: -o[0]):
        out[i1:i2] = rep
    return out

def main(src, dst):
    raw = open(src, 'rb').read()
    assert hashlib.sha256(raw).hexdigest() == EXPECT_IN, '輸入不是 v649（SHA256 不符）'
    spec = importlib.util.spec_from_file_location('s649', src); s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    cod = types.ModuleType('dict_v14_codec'); exec(s._unz(s._PACK['dict_v14_codec.py']).decode('utf-8'), cod.__dict__)
    t = tempfile.NamedTemporaryFile(suffix='_columnar.json', delete=False); t.write(s._unz(s._PACK['回填原因處置字典_v99_columnar.json'])); t.close()
    D = cod.load_any(t.name)
    R = D['rule_R_1006_17'].pop('pending_6b_new_keys_resolved')
    for k in R['created']:
        del D['orders'][k]
    for k in ('8926077572', '8926070495'):
        r = D['orders'][k]; r['disp_zh'] = r.pop('disp_zh_before_r1006_20'); r.pop('r1006_20'); r.pop('directive')
    D['rule_R_0917_33'].pop('amended_by_R_1006_18'); D.pop('rule_R_1006_18_21'); D.pop('note_v99')
    D['version'] = 'v98'; D['count'] = len(D['orders'])
    dct = json.dumps(cod.encode(D), ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    bld = '\n'.join(apply(s._unz(s._PACK['build_dpr.py']).decode('utf-8').split('\n'), PATCH['build_dpr.py'])).encode('utf-8')
    rep = {"    '回填原因處置字典_v99_columnar.json': '": "    '回填原因處置字典_v98_columnar.json': '%s'," % s._z(dct),
           "    'build_dpr.py': '": "    'build_dpr.py': '%s'," % s._z(bld)}
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
    print(h, '✅ v648 逐位元組相同' if h == EXPECT_OUT else '❌ 不符')
    return h == EXPECT_OUT

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
